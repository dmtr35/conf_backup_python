from setting.set_data import save_system_info, collect_metadata
from setting.decor_permission import copy, rmtree
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


def scan_config(paths: list):
    now = datetime.now()
    date_string = now.strftime("_%d.%m.%Y_%H-%M")
    tmp_folder = "/tmp/conf_backup" + date_string
    metadata_file = os.path.join(tmp_folder, "metadata.json")
    os.makedirs(tmp_folder, exist_ok=True)

    host_name = save_system_info(tmp_folder)
    
    listignore = os.path.join(os.getcwd(), ".listignore")
    if os.path.isfile(listignore):
        with open(listignore, 'r') as f:                                         # Загружаем конфигурацию из файла
            ignore_patterns = [line.strip() for line in f if line.strip()]
    else:
        ignore_patterns = []

    metadata = {}
    for src_path in paths:
        replace_path = src_path.replace('/', '*')
        dest_base = os.path.join(tmp_folder, replace_path)
        if os.path.isdir(src_path):
            collect_metadata(src_path, metadata)
            for dirpath, dirnames, filenames in os.walk(src_path):
                replace_path = dirpath.replace('/', '*')
                rel_path = os.path.relpath(dirpath, src_path)

                if not rel_path == ".":
                    rel_path = change_folder_name(rel_path.split('/'), replace_path)
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
                    copy(src_file, dest_file)
        else:
            if os.path.isfile(src_path):
                if check_listignore(src_path, ignore_patterns):             # проверка файла на ignore_patterns
                    continue
                collect_metadata(src_path, metadata)
                copy(src_path, dest_base)

    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)

    folder_name = os.path.basename(tmp_folder)
    backup_file_path = os.path.join(".", f"{folder_name}_{host_name}.tar.gz")

    with tarfile.open(backup_file_path, "w:gz") as tar:
        tar.add(tmp_folder, arcname=".")

    rmtree(tmp_folder)
    # shutil.rmtree(tmp_folder)

