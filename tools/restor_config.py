from setting.decor_permission import copy, rmtree, restor_metadata
import os
import json
import tarfile

def parse_path(dir_data):
    return dir_data.replace("*", "/")

def restor_config(recovery_file):
    if not os.path.exists(recovery_file):
        print(f"file <{recovery_file}> doesn't exist")
        return
    
    tmp_folder = os.path.join("/tmp", recovery_file).removesuffix(".tar.gz")

    with tarfile.open(recovery_file, "r:gz") as tar:
        tar.extractall(path=tmp_folder)

    metadata_path = os.path.join(tmp_folder, "metadata.json")

    with open(metadata_path, 'r') as f:                                 # Загружаем конфигурацию из файла
        metadata_file = json.load(f)

    for dirpath, dirnames, filenames in os.walk(tmp_folder):
        for dir_data in dirnames:
            dir_path = parse_path(dir_data)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                restor_metadata(dir_path, metadata_file)
            restor_metadata(dir_path, metadata_file)

        for dir_data in filenames:
            if dir_data == "metadata.json" or dir_data == "system_info.txt":
                continue
            file_path = parse_path(dir_data)
            if os.path.exists(file_path):
                copy(file_path, file_path + "_copy")
            copy(os.path.join(dirpath, dir_data), file_path)
            restor_metadata(file_path, metadata_file)

    rmtree(tmp_folder)
