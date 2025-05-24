import tarfile
import filecmp
import os
from setting.decor_permission import rmtree

def is_changed(dir1, dir2, ignore, changes=None):
    if changes is None:
        changes = {
            "added": [],
            "deleted": [],
            "changed": [],
        }

    comparison = filecmp.dircmp(dir1, dir2, ignore=ignore)

    changes["added"].extend(comparison.left_only)
    changes["deleted"].extend(comparison.right_only)

    for common_file in comparison.common_files:
        file1 = os.path.join(dir1, common_file)
        file2 = os.path.join(dir2, common_file)
        if not filecmp.cmp(file1, file2, shallow=False):
            changes["changed"].append(common_file)

    for subdir in comparison.subdirs:
        is_changed(
            os.path.join(dir1, subdir),
            os.path.join(dir2, subdir),
            ignore,
            changes                                           # передаём один и тот же словарь
        )

    return changes

def check_change_config(tmp_folder, old_backup, ignore):
    tmp_old_backup = "/tmp/conf_backup.bak"

    with tarfile.open(old_backup, "r:gz") as tar:
        tar.extractall(path=tmp_old_backup)

    changes = is_changed(tmp_folder, tmp_old_backup, ignore)
    changes["added"] = [os.path.basename(change.replace('*', '/')) for change in changes["added"]]
    changes["deleted"] = [os.path.basename(change.replace('*', '/')) for change in changes["deleted"]]
    changes["changed"] = [os.path.basename(change.replace('*', '/')) for change in changes["changed"]]
    
    if changes["added"]:
        print("Added files:", changes["added"])
    if changes["deleted"]:
        print("Deleted files:", changes["deleted"])
    if changes["changed"]:
        print("Changed files:", changes["changed"])
    if not any(changes.values()):
        print("No changes.")

    res = not any(changes.values())
    rmtree(tmp_old_backup)
    return res
    