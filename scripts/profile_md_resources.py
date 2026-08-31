#!/usr/bin/env python3
"""Inventory local MD resources and project capacity from an optional measured benchmark."""

from __future__ import annotations

import argparse
import ctypes
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ENGINE_COMMANDS = {
    "gmx": ["gmx", "--version"],
    "gmx_mpi": ["gmx_mpi", "--version"],
    "openmm": [sys.executable, "-c", "import openmm; print(openmm.__version__)"],
    "namd3": ["namd3", "--version"],
    "namd2": ["namd2", "--version"],
    "pmemd.cuda": ["pmemd.cuda", "-h"],
    "pmemd": ["pmemd", "-h"],
    "lmp": ["lmp", "-h"],
}


def run_text(command: list[str]) -> str | None:
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=8,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def memory_bytes() -> tuple[int | None, int | None]:
    try:
        import psutil  # type: ignore

        vm = psutil.virtual_memory()
        return int(vm.total), int(vm.available)
    except Exception:
        pass
    if os.name == "posix" and hasattr(os, "sysconf"):
        try:
            page = int(os.sysconf("SC_PAGE_SIZE"))
            total = page * int(os.sysconf("SC_PHYS_PAGES"))
            available = page * int(os.sysconf("SC_AVPHYS_PAGES"))
            return total, available
        except (ValueError, OSError):
            pass
    if os.name == "nt":
        class MemoryStatus(ctypes.Structure):
            _fields_ = [
                ("length", ctypes.c_ulong),
                ("memory_load", ctypes.c_ulong),
                ("total_physical", ctypes.c_ulonglong),
                ("available_physical", ctypes.c_ulonglong),
                ("total_page_file", ctypes.c_ulonglong),
                ("available_page_file", ctypes.c_ulonglong),
                ("total_virtual", ctypes.c_ulonglong),
                ("available_virtual", ctypes.c_ulonglong),
                ("available_extended_virtual", ctypes.c_ulonglong),
            ]

        status = MemoryStatus()
        status.length = ctypes.sizeof(MemoryStatus)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return int(status.total_physical), int(status.available_physical)
    return None, None


def physical_cpu_count() -> int | None:
    try:
        import psutil  # type: ignore

        value = psutil.cpu_count(logical=False)
        return int(value) if value else None
    except Exception:
        pass
    if os.name == "posix":
        output = run_text(["lscpu", "-p=socket,core"])
        if output:
            cores = {line for line in output.splitlines() if line and not line.startswith("#")}
            return len(cores) or None
    if os.name == "nt":
        output = run_text(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                "(Get-CimInstance Win32_Processor | Measure-Object -Property NumberOfCores -Sum).Sum",
            ]
        )
        try:
            return int(output) if output else None
        except ValueError:
            return None
    return None


def md_engine_inventory() -> list[dict[str, Any]]:
    engines: list[dict[str, Any]] = []
    for name, command in ENGINE_COMMANDS.items():
        executable = shutil.which(command[0])
        if not executable:
            continue
        output = run_text([executable, *command[1:]])
        if name == "openmm" and not output:
            # The Python executable exists even when the OpenMM module does not.
            # Do not report that interpreter path as an installed MD engine.
            continue
        engines.append(
            {
                "name": name,
                "executable": executable,
                "version_probe": command[1:],
                "version_output": output[:1200] if output else None,
                "availability": "AVAILABLE" if output else "EXECUTABLE_FOUND_VERSION_UNKNOWN",
            }
        )
    return engines


def nvidia_inventory() -> list[dict[str, Any]]:
    nvidia_smi = shutil.which("nvidia-smi")
    if not nvidia_smi and os.name == "nt":
        candidates = [
            Path(os.environ.get("WINDIR", r"C:\Windows")) / "System32" / "nvidia-smi.exe",
            Path(r"C:\Program Files\NVIDIA Corporation\NVSMI\nvidia-smi.exe"),
        ]
        nvidia_smi = next((str(path) for path in candidates if path.exists()), None)
    if not nvidia_smi:
        return []
    output = run_text(
        [
            nvidia_smi,
            "--query-gpu=index,name,memory.total,memory.free,driver_version",
            "--format=csv,noheader,nounits",
        ]
    )
    if not output:
        return []
    devices: list[dict[str, Any]] = []
    for line in output.splitlines():
        fields = [field.strip() for field in line.split(",")]
        if len(fields) != 5:
            continue
        index, name, total_mb, free_mb, driver = fields
        devices.append(
            {
                "backend": "nvidia",
                "index": int(index),
                "name": name,
                "memory_total_mb": int(total_mb),
                "memory_free_mb": int(free_mb),
                "driver_version": driver,
            }
        )
    return devices


def amd_inventory() -> list[dict[str, Any]]:
    output = run_text(["rocm-smi", "--showproductname", "--showmeminfo", "vram", "--json"])
    if not output:
        return []
    try:
        parsed = json.loads(output)
    except json.JSONDecodeError:
        return [{"backend": "amd", "raw_inventory": output}]
    return [{"backend": "amd", "raw_inventory": parsed}]


def windows_display_inventory() -> list[dict[str, Any]]:
    if os.name != "nt":
        return []
    output = run_text(
        [
            "powershell.exe",
            "-NoProfile",
            "-Command",
            "Get-CimInstance Win32_VideoController | Select-Object Name,AdapterRAM,DriverVersion,Status | ConvertTo-Json -Compress",
        ]
    )
    if not output:
        return []
    try:
        values = json.loads(output)
    except json.JSONDecodeError:
        return [{"backend": "windows_display_adapter", "raw_inventory": output}]
    if isinstance(values, dict):
        values = [values]
    devices = []
    for index, value in enumerate(values):
        devices.append(
            {
                "backend": "windows_display_adapter",
                "index": index,
                "name": value.get("Name"),
                "adapter_ram_bytes_reported": value.get("AdapterRAM"),
                "driver_version": value.get("DriverVersion"),
                "status": value.get("Status"),
                "warning": "Win32_VideoController inventory does not prove CUDA/ROCm compute availability or reliable usable VRAM.",
            }
        )
    return devices


def project_benchmark(args: argparse.Namespace) -> dict[str, Any] | None:
    supplied = [args.benchmark_ns, args.wall_hours, args.output_bytes]
    if not any(value is not None for value in supplied):
        return None
    if args.benchmark_ns is None or args.wall_hours is None:
        raise SystemExit("--benchmark-ns and --wall-hours must be supplied together")
    if args.benchmark_ns <= 0 or args.wall_hours <= 0:
        raise SystemExit("benchmark duration and wall time must be positive")
    ns_per_day = args.benchmark_ns / args.wall_hours * 24.0
    bytes_per_ns = None
    if args.output_bytes is not None:
        if args.output_bytes < 0:
            raise SystemExit("--output-bytes cannot be negative")
        bytes_per_ns = args.output_bytes / args.benchmark_ns
    targets = sorted({1.0, 10.0, 100.0, *args.target_ns})
    projections = []
    for target in targets:
        if target <= 0:
            raise SystemExit("all --target-ns values must be positive")
        wall_hours = target / ns_per_day * 24.0 * args.replicates
        parallel_batches = (args.replicates + args.concurrent_replicates - 1) // args.concurrent_replicates
        parallel_wall_hours = target / ns_per_day * 24.0 * parallel_batches
        storage_bytes = None if bytes_per_ns is None else bytes_per_ns * target * args.replicates
        projections.append(
            {
                "target_ns_per_replicate": target,
                "replicates": args.replicates,
                "projected_wall_hours_at_serial_throughput": wall_hours,
                "concurrent_replicates": args.concurrent_replicates,
                "projected_wall_hours_at_declared_concurrency": parallel_wall_hours,
                "projected_storage_bytes": storage_bytes,
            }
        )
    return {
        "basis": "measured_benchmark_values_supplied_by_caller",
        "benchmark_ns": args.benchmark_ns,
        "wall_hours": args.wall_hours,
        "ns_per_day": ns_per_day,
        "output_bytes": args.output_bytes,
        "bytes_per_ns": bytes_per_ns,
        "atom_count": args.atom_count,
        "engine": args.engine,
        "device": args.device,
        "projections": projections,
        "warning": "Projection is arithmetic, not a scientific sufficiency decision. Validate system, parameters, convergence and replicate design separately.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    parser.add_argument("--benchmark-ns", type=float)
    parser.add_argument("--wall-hours", type=float)
    parser.add_argument("--output-bytes", type=int)
    parser.add_argument("--atom-count", type=int)
    parser.add_argument("--engine")
    parser.add_argument("--device")
    parser.add_argument("--replicates", type=int, default=1)
    parser.add_argument("--concurrent-replicates", type=int, default=1)
    parser.add_argument("--target-ns", type=float, action="append", default=[])
    args = parser.parse_args()
    if args.replicates < 1:
        raise SystemExit("--replicates must be at least 1")
    if args.concurrent_replicates < 1 or args.concurrent_replicates > args.replicates:
        raise SystemExit("--concurrent-replicates must be between 1 and --replicates")

    task_root = args.task_root.resolve()
    total_memory, available_memory = memory_bytes()
    disk = shutil.disk_usage(task_root)
    accelerators = nvidia_inventory() + amd_inventory()
    if not accelerators:
        accelerators = windows_display_inventory()
    payload = {
        "schema_version": "plant_md_resource_profile_v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "task_root": str(task_root),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
            "wsl": bool(os.environ.get("WSL_DISTRO_NAME")),
            "wsl_distro": os.environ.get("WSL_DISTRO_NAME"),
        },
        "cpu": {
            "physical_count": physical_cpu_count(),
            "logical_count": os.cpu_count(),
            "processor": platform.processor() or None,
        },
        "memory": {
            "total_bytes": total_memory,
            "available_bytes": available_memory,
        },
        "disk": {
            "total_bytes": disk.total,
            "used_bytes": disk.used,
            "free_bytes": disk.free,
        },
        "accelerators": accelerators,
        "md_engines": md_engine_inventory(),
        "benchmark": project_benchmark(args),
        "scope_note": "This script inventories local resources and performs arithmetic capacity projections. It does not build a system, validate parameter coverage, run an engine benchmark, or complete Q0/Q2 by itself.",
        "decision_boundary": {
            "gpu_absence_is_scientific_negative": False,
            "gpu_presence_authorizes_production_md": False,
            "production_requires": [
                "named_discriminating_question",
                "complete_parameterization",
                "geometry_and_setup_qc",
                "measured_system_specific_benchmark",
                "projected_time_memory_and_storage_budget",
                "persisted_user_decision",
            ],
        },
    }
    encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
