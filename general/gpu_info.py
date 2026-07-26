#!/usr/bin/env python3
"""
gpu_info.py — Prints GPU/NVIDIA/CUDA/Docker-GPU info on a Linux machine.

Usage: python gpu_info.py

No third-party dependencies required. Uses standard shell tools when available:
    lspci, nvidia-smi, nvcc, docker, dpkg
"""

from __future__ import annotations

import shutil
import subprocess
from typing import Optional


def run(cmd: list[str], timeout: int = 10) -> tuple[int, str, str]:
    try:
        p = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )

        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except FileNotFoundError:
        return 127, "", f"{cmd[0]}: not found"
    except subprocess.TimeoutExpired:
        return 124, "", f"{cmd[0]}: timed out"
    except Exception as e:  # pragma: no cover
        return 1, "", str(e)


def have(binary: str) -> bool:
    return shutil.which(binary) is not None


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def detect_gpus() -> list[str]:
    if not have("lspci"):
        return []

    rc, out, _ = run(["lspci"])

    if rc != 0:
        return []

    keywords = ("VGA", "3D controller", "Display controller")

    return [line for line in out.splitlines() if any(k in line for k in keywords)]


def nvidia_smi_query(fields: str) -> Optional[list[list[str]]]:
    if not have("nvidia-smi"):
        return None

    rc, out, _ = run(
        ["nvidia-smi", f"--query-gpu={fields}", "--format=csv,noheader,nounits"]
    )

    if rc != 0 or not out:
        return None

    return [[cell.strip() for cell in line.split(",")] for line in out.splitlines()]


def get_driver_and_cuda() -> tuple[Optional[str], Optional[str]]:
    if not have("nvidia-smi"):
        return None, None

    rc, out, _ = run(["nvidia-smi"])

    if rc != 0:
        return None, None

    driver = cuda = None

    for line in out.splitlines():
        if "Driver Version:" in line and "CUDA Version:" in line:
            # e.g.  "| NVIDIA-SMI 580.142   Driver Version: 580.142   CUDA Version: 13.0  |"
            parts = line.replace("|", " ").split()

            try:
                driver = parts[parts.index("Version:") + 1]
                # find next "Version:" after that for CUDA
                cuda_idx = parts.index("Version:", parts.index("Version:") + 1)
                cuda = parts[cuda_idx + 1]
            except (ValueError, IndexError):
                pass
            break

    return driver, cuda


def get_nvcc_version() -> Optional[str]:
    if not have("nvcc"):
        return None

    rc, out, _ = run(["nvcc", "--version"])

    if rc != 0:
        return None

    for line in out.splitlines():
        if "release" in line.lower():
            return line.strip()

    return out.splitlines()[-1] if out else None


def check_container_toolkit() -> dict[str, object]:
    info: dict[str, object] = {
        "nvidia_ctk": have("nvidia-ctk"),
        "nvidia_container_runtime": have("nvidia-container-runtime"),
        "docker": have("docker"),
        "docker_has_nvidia_runtime": False,
        "toolkit_pkg_version": None,
    }

    if have("dpkg"):
        rc, out, _ = run(["dpkg", "-s", "nvidia-container-toolkit"])

        if rc == 0:
            for line in out.splitlines():
                if line.startswith("Version:"):
                    info["toolkit_pkg_version"] = line.split(":", 1)[1].strip()
                    break

    if have("docker"):
        rc, out, _ = run(["docker", "info"])

        if rc == 0:
            for line in out.splitlines():
                if line.strip().startswith("Runtimes:") and "nvidia" in line:
                    info["docker_has_nvidia_runtime"] = True
                    break

    return info


def main() -> int:
    section("Hardware (lspci)")

    gpus = detect_gpus()

    if not gpus:
        print("No GPU detected via lspci (or lspci is unavailable).")
    else:
        for line in gpus:
            print(line)

    has_nvidia_hw = any("NVIDIA" in g.upper() for g in gpus)

    section("NVIDIA driver / CUDA runtime")

    if not have("nvidia-smi"):
        if has_nvidia_hw:
            print("NVIDIA GPU present, but 'nvidia-smi' is NOT installed.")
            print("=> No NVIDIA driver detected. Install the NVIDIA driver to use CUDA.")
        else:
            print("You do NOT have an NVIDIA GPU (nor NVIDIA driver).")

        # CUDA toolkit still worth reporting
        nvcc = get_nvcc_version()
        if nvcc:
            print(f"CUDA toolkit (nvcc): {nvcc}")
        else:
            print("CUDA toolkit (nvcc): not installed")

        section("Container GPU support")
        _print_container(check_container_toolkit())

        return 0

    driver, cuda = get_driver_and_cuda()

    print(f"Driver version           : {driver or 'unknown'}")
    print(f"Max CUDA supported (drv) : {cuda or 'unknown'}")

    nvcc = get_nvcc_version()
    print(f"CUDA toolkit (nvcc)      : {nvcc or 'not installed'}")

    if cuda:
        try:
            major, minor = (int(x) for x in cuda.split(".")[:2])
            ok = (major, minor) >= (12, 4)
            print(
                f"CUDA 12.4 compatible     : {'YES' if ok else 'NO'} "
                f"(driver reports {cuda})"
            )
        except ValueError:
            pass

    section("GPUs")
    rows = nvidia_smi_query("index,name,memory.total,compute_cap,uuid")

    if not rows:
        print("nvidia-smi query failed.")
    else:
        total_mem_mib = 0
        for idx, name, mem_mib, cc, uuid in rows:
            try:
                mem_val = int(mem_mib)
                total_mem_mib += mem_val
                mem_str = f"{mem_val / 1024:.2f} GB ({mem_val} MiB)"
            except ValueError:
                mem_str = f"{mem_mib} MiB"
            print(f"[{idx}] {name}")
            print(f"      Memory       : {mem_str}")
            print(f"      Compute cap. : {cc}")
            print(f"      UUID         : {uuid}")
        if len(rows) > 1:
            print(f"\nTotal GPU memory across {len(rows)} GPUs: "
                  f"{total_mem_mib / 1024:.2f} GB")

    section("Container GPU support")
    _print_container(check_container_toolkit())

    return 0


def _print_container(info: dict[str, object]) -> None:
    ver = info["toolkit_pkg_version"]

    print(f"nvidia-container-toolkit : "
          f"{'installed (' + str(ver) + ')' if ver else 'not installed'}")
    print(f"nvidia-ctk binary        : {'yes' if info['nvidia_ctk'] else 'no'}")
    print(f"nvidia-container-runtime : "
          f"{'yes' if info['nvidia_container_runtime'] else 'no'}")
    print(f"docker installed         : {'yes' if info['docker'] else 'no'}")

    if info["docker"]:
        print(f"docker 'nvidia' runtime  : "
              f"{'configured' if info['docker_has_nvidia_runtime'] else 'NOT configured'}")


if __name__ == "__main__":
    raise SystemExit(main())
