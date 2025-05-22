import tarfile
import filecmp
from setting.decor_permission import rmtree

def check_change_config(tmp_folder, old_backup, ignore):
    tmp_old_backup = "/tmp/conf_backup.bak"

    with tarfile.open(old_backup, "r:gz") as tar:
        tar.extractall(path=tmp_old_backup)

    comparison = filecmp.dircmp(tmp_folder, tmp_old_backup, ignore)
    res = not (comparison.left_only or comparison.right_only or comparison.diff_files)
    rmtree(tmp_old_backup)
    return res
    