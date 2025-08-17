from setting.decor_permission import copy, restor_metadata
import os
from pathlib import Path
import json

def parse_path(dir_data):
    return dir_data.replace("*", "/")


def restore_dirs(recovery_dir, bool_res_list, restore_list, metadata_file, save_original):
    for dirpath, dirnames, filenames in os.walk(recovery_dir):
        for dir_data in dirnames:
            if bool_res_list:
                if dir_data in restore_list:
                    restore_dir(dir_data, metadata_file)
                    restore_dirs(Path(dirpath) / dir_data, 0, restore_list, metadata_file, save_original)
            else:
                restore_dir(dir_data, metadata_file)

        for dir_data in filenames:
            if bool_res_list:
                if dir_data in restore_list:
                    restore_file(dir_data, dirpath, metadata_file, save_original)
            else:
                restore_file(dir_data, dirpath, metadata_file, save_original)


def restore_dir(dir_data, metadata_file):
    dir_path = Path(parse_path(dir_data))
    if not dir_path.exists():
        dir_path.mkdir(exist_ok=True)
        restor_metadata(dir_path, metadata_file)
    restor_metadata(dir_path, metadata_file)


def restore_file(dir_data, dirpath, metadata_file, save_original):
    if dir_data == "metadata.json" or dir_data == "system_info.txt" or dir_data == "config.json" or dir_data == "restore_list.json":
        return
    file_path = Path(parse_path(dir_data))
    dir_name_path = file_path.parent
    if file_path.exists() and save_original:
        copy(file_path, file_path + ".bak")
    if not dir_name_path.exists():
        dir_name_path.mkdir(exist_ok=True)
    copy(Path(dirpath) / dir_data, file_path)
    restor_metadata(file_path, metadata_file)


def restore_config(recovery_dir, config_path, save_original):
    if not Path(recovery_dir).exists():
        print(f"file <{recovery_dir}> doesn't exist")
        return
    
    bool_res_list = 0

    with open(config_path, 'r') as f:                                 # Загружаем конфигурацию из файла
        config = json.load(f)
    restore_list = [p for p in config['restore_list']]
    if restore_list:
        bool_res_list = 1


    metadata_path = Path(recovery_dir) / "metadata.json"
    with open(str(metadata_path), 'r') as f:                                 # Загружаем конфигурацию из файла
        metadata_file = json.load(f)

    restore_dirs(recovery_dir, bool_res_list, restore_list, metadata_file, save_original)
