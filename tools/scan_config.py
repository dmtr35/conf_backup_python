from setting.set_data import get_system_info, save_system_info, collect_metadata, collect_restore_list
from setting.decor_permission import copy, rmtree
from pathlib import Path
import os
import json
import fnmatch

def check_listignore(path_file, ignore_patterns):
    return any(fnmatch.fnmatch(path_file, pattern) for pattern in ignore_patterns) or path_file.is_symlink()


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
    info = get_system_info()
    path_conf = Path(script_dir) / f"conf_backup_{info['hostname']}"

    if path_conf.exists():
        rmtree(str(path_conf))
    path_conf.mkdir()

    save_system_info(path_conf, info)

    metadata_file = path_conf / "metadata.json"
    restore_list_file = path_conf / "restore_list.json"

    copy(config_path, path_conf / "config.json")

    with open(config_path, 'r') as f:                                 # Загружаем конфигурацию из файла
        config = json.load(f)
    config_paths = [p for p in config['config_paths']]
    ignore_patterns = [p for p in config['listignore']]
    paths = [Path(path) for path in config_paths if Path(path).exists()]

    
    restore_list = []
    metadata = {}
    for src_path in paths:
        replace_path = str(src_path).replace('/', '*')
        dest_base = path_conf / replace_path
        if src_path.is_dir():
            collect_restore_list(replace_path, restore_list)
            collect_metadata(str(src_path), metadata)
            for dirpath, dirnames, filenames in os.walk(src_path):
                replace_path = dirpath.replace('/', '*')
                rel_path = Path(os.path.relpath(dirpath, src_path))

                if not str(rel_path) == ".":
                    rel_path = change_folder_name(str(rel_path).split('/'), replace_path)

                    collect_restore_list(replace_path, restore_list)
                dest_path = dest_base / rel_path

                if check_listignore(Path(dirpath), ignore_patterns):              # проверка папки на ignore_patterns
                    continue

                if not str(dest_path).endswith("/.") and not dest_path.parent.is_dir:
                    continue
                dest_path.mkdir(exist_ok=True)

                # Сохраняем метаданные для директорий
                for dir in dirnames:
                    src_dir = Path(dirpath) / dir
                    if check_listignore(src_dir, ignore_patterns):          # проверка папки на ignore_patterns
                        continue
                    collect_metadata(str(src_dir), metadata)

                # Копируем файлы
                for filename in filenames:
                    src_file = Path(dirpath) / filename
                    replace_path = str(src_file).replace('/', '*')
                    if check_listignore(src_file, ignore_patterns):         # проверка файла на ignore_patterns
                        continue

                    collect_metadata(str(src_file), metadata)
                    dest_file = dest_path / replace_path
                    collect_restore_list(dest_file.name, restore_list)
                    copy(src_file, dest_file)
        elif src_path.is_file:
                if check_listignore(src_path, ignore_patterns):             # проверка файла на ignore_patterns
                    continue
                collect_restore_list(dest_base.name, restore_list)
                collect_metadata(str(src_path), metadata)
                copy(src_path, dest_base)

    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)
    with open(restore_list_file, 'w') as f:
        json.dump(restore_list, f, indent=4)

    print(f"=== Backup folder '{path_conf.name}' created ===")

