import os
import platform
import sys
import json
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

def save_system_info(backup_dir):
    info = get_system_info()
    info_file = os.path.join(backup_dir, "system_info.txt")
    with open(info_file, "w") as f:
        for key, value in info.items():
            f.write(f"{key}: {value}\n")
    return info["hostname"]


def collect_metadata(path, metadata):
    if os.path.exists(path):
        stat_info = os.stat(path)
        metadata[path] = {
            'uid': stat_info.st_uid,
            'gid': stat_info.st_gid,
            'mode': oct(stat_info.st_mode)
        }


