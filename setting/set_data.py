from pathlib import Path
import platform
import sys
from datetime import datetime

def get_system_info():
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "hostname": platform.node(),
        "kernel_version": platform.release(),
        "python_version": sys.version,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def save_system_info(backup_dir, info):
    info_file = Path(backup_dir) / "system_info.txt"
    with info_file.open("w") as f:
        for key, value in info.items():
            f.write(f"{key}: {value}\n")
    return info["hostname"]


def collect_metadata(path, metadata):
    p = Path(path)
    if p.exists():
        stat_info = p.stat()
        metadata[str(p)] = {
            'uid': stat_info.st_uid,
            'gid': stat_info.st_gid,
            'mode': oct(stat_info.st_mode)
        }

def collect_restore_list(name, restore_list):
    restore_list.append(name)

