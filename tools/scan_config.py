from setting.set_data import save_system_info, collect_metadata, collect_restore_list
from setting.decor_permission import copy, rmtree
from setting.check_backup import check_change_config
import os
import json
import tarfile
from datetime import datetime
import fnmatch

def check_listignore(path_file, ignore_patterns):
    return any(fnmatch.fnmatch(path_file, pattern) for pattern in ignore_patterns) or os.path.islink(path_file)


def change_folder_name(arr_folder_names, replace_path):
    if len(arr_folder_names) == 1:
        return replace_path
    else:
        new_path = "" 
        for i in range(len(arr_folder_names) - 1, -1, -1):
            new_path = replace_path + "/" + new_path
            replace_path = replace_path.rsplit("*", 1)[0]
        return new_path.rstrip('/')


def scan_config(config_path, script_dir):
    now = datetime.now()
    date_string = now.strftime("_%d.%m.%Y")
    tmp_folder = "/tmp/conf_backup" + date_string
    metadata_file = os.path.join(tmp_folder, "metadata.json")
    restore_list_file = os.path.join(tmp_folder, "restore_list.json")
    os.makedirs(tmp_folder, exist_ok=True)

    copy(config_path, os.path.join(tmp_folder, "config.json"))

    with open(config_path, 'r') as f:                                 # Загружаем конфигурацию из файла
        config = json.load(f)
    config_paths = [p for p in config['config_paths']]
    ignore_patterns = [p for p in config['listignore']]
    paths = [path for path in config_paths if os.path.exists(path)]

    host_name = save_system_info(tmp_folder)
    
    restore_list = []
    metadata = {}
    for src_path in paths:
        replace_path = src_path.replace('/', '*')
        dest_base = os.path.join(tmp_folder, replace_path)
        if os.path.isdir(src_path):
            collect_restore_list(replace_path, restore_list)
            collect_metadata(src_path, metadata)
            for dirpath, dirnames, filenames in os.walk(src_path):
                replace_path = dirpath.replace('/', '*')
                rel_path = os.path.relpath(dirpath, src_path)

                if not rel_path == ".":
                    rel_path = change_folder_name(rel_path.split('/'), replace_path)

                    collect_restore_list(replace_path, restore_list)
                dest_path = os.path.join(dest_base, rel_path)

                if check_listignore(dirpath, ignore_patterns):              # проверка папки на ignore_patterns
                    continue

                if not dest_path.endswith("/.") and not os.path.isdir(os.path.dirname(dest_path)):
                    continue
                os.makedirs(dest_path, exist_ok=True)

                # Сохраняем метаданные для директорий
                for dir in dirnames:
                    src_dir = os.path.join(dirpath, dir)
                    if check_listignore(src_dir, ignore_patterns):          # проверка папки на ignore_patterns
                        continue
                    collect_metadata(src_dir, metadata)

                # Копируем файлы
                for filename in filenames:
                    src_file = os.path.join(dirpath, filename)
                    replace_path = src_file.replace('/', '*')
                    if check_listignore(src_file, ignore_patterns):         # проверка файла на ignore_patterns
                        continue

                    collect_metadata(src_file, metadata)
                    dest_file = os.path.join(dest_path, replace_path)
                    collect_restore_list(os.path.basename(dest_file), restore_list)
                    copy(src_file, dest_file)
        else:
            if os.path.isfile(src_path):
                if check_listignore(src_path, ignore_patterns):             # проверка файла на ignore_patterns
                    continue
                collect_metadata(src_path, metadata)
                collect_restore_list(os.path.basename(dest_base), restore_list)
                copy(src_path, dest_base)


    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)
    with open(restore_list_file, 'w') as f:
        json.dump(restore_list, f, indent=4)

    olds_backups = [os.path.join(script_dir, backup) for backup in os.listdir(script_dir) if backup.endswith(".tar.gz")]

    if olds_backups:
        old_backup = max(olds_backups, key=lambda f: os.stat(f).st_mtime)
        ignored_files = ["system_info.txt"]
        if check_change_config(tmp_folder, old_backup, ignore=ignored_files):
            rmtree(tmp_folder)
            print("=== No changes in configuration files ===")
            return 

    folder_name = os.path.basename(tmp_folder)
    backup_file_path = os.path.join(script_dir, f"{folder_name}_{host_name}.tar.gz")

    with tarfile.open(backup_file_path, "w:gz") as tar:
        tar.add(tmp_folder, arcname=".")
    print(f"=== Backup file '{os.path.basename(backup_file_path)}' created ===")

    rmtree(tmp_folder)

