import os
from pathlib import Path
import shutil


def decor_permission(fun):
    def wrapper(*args):
        try:
            return fun(*args)
        except Exception as e:
            print(f"[{fun.__name__}] Operation not permitted: {e}")
    return wrapper


@decor_permission
def copy(src_file, dest_file):
    shutil.copy2(src_file, dest_file)

@decor_permission
def rmtree(folder):
    shutil.rmtree(folder)

@decor_permission
def restor_metadata(path, metadata_files):
    p = Path(path)
    metadata = metadata_files[str(p)]
    mode = int(metadata["mode"], 8)
    uid = int(metadata["uid"])
    gid = int(metadata["gid"])
    
    p.chmod(mode) 
    os.chown(p, uid, gid)
