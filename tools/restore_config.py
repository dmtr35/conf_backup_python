from setting.decor_permission import copy, rmtree, restor_metadata
import os
import json
import tarfile

def parse_path(dir_data):
    return dir_data.replace("*", "/")


def restore_dirs(tmp_folder, bool_res_list, restore_list, metadata_file, save_original):
    for dirpath, dirnames, filenames in os.walk(tmp_folder):
        for dir_data in dirnames:
            if bool_res_list:
                if dir_data in restore_list:
                    restore_dir(dir_data, metadata_file)
                    restore_dirs(os.path.join(dirpath, dir_data), 0, restore_list, metadata_file, save_original)
            else:
                restore_dir(dir_data, metadata_file)

        for dir_data in filenames:
            if bool_res_list:
                if dir_data in restore_list:
                    restore_file(dir_data, dirpath, metadata_file, save_original)
            else:
                restore_file(dir_data, dirpath, metadata_file, save_original)


def restore_dir(dir_data, metadata_file):
    dir_path = parse_path(dir_data)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        restor_metadata(dir_path, metadata_file)
    restor_metadata(dir_path, metadata_file)


def restore_file(dir_data, dirpath, metadata_file, save_original):
    if dir_data == "metadata.json" or dir_data == "system_info.txt" or dir_data == "config.json" or dir_data == "restore_list.json":
        return
    file_path = parse_path(dir_data)
    dir_name_path = os.path.dirname(file_path)
    if os.path.exists(file_path) and save_original:
        copy(file_path, file_path + ".bak")
    if not os.path.exists(dir_name_path):
        os.makedirs(dir_name_path, exist_ok=True)
    copy(os.path.join(dirpath, dir_data), file_path)
    restor_metadata(file_path, metadata_file)


def restore_config(recovery_file, config_path, save_original):
    if not os.path.exists(recovery_file):
        print(f"file <{recovery_file}> doesn't exist")
        return
    
    tmp_folder = os.path.join("/tmp", recovery_file).removesuffix(".tar.gz")

    with open(config_path, 'r') as f:                                 # Загружаем конфигурацию из файла
        config = json.load(f)
    restore_list = [p for p in config['restore_list']]
    bool_res_list = 0
    if restore_list:
        bool_res_list = 1

    with tarfile.open(recovery_file, "r:gz") as tar:
        tar.extractall(path=tmp_folder)

    metadata_path = os.path.join(tmp_folder, "metadata.json")

    with open(metadata_path, 'r') as f:                                 # Загружаем конфигурацию из файла
        metadata_file = json.load(f)

    restore_dirs(tmp_folder, bool_res_list, restore_list, metadata_file, save_original)

    rmtree(tmp_folder)
