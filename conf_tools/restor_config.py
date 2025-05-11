import os
import json
import sys
from datetime import datetime
import tarfile






def restor_config(recovery_file):
    if not os.path.exists(recovery_file):
        print(f"file <{recovery_file}> doesn't exist")
        return
    
    tmp_path = os.path.join("/tmp", recovery_file).removesuffix(".tar.gz")

    with tarfile.open(recovery_file, "r:gz") as tar:
        tar.extractall(path=tmp_path)
        print(f"файл распакован в {tmp_path}")

    metadata_path =os.path.join(tmp_path, "metadata.json")
    list_files = [os.path.join(tmp_path, f) for f in os.listdir(tmp_path) if f not in {"metadata.json", "system_info.txt"}]

    with open(metadata_path, 'r') as f:                                 # Загружаем конфигурацию из файла
        metadata_file = json.load(f)
    metadata_file_names = [file_name for file_name in metadata_file.keys()]

    # for dirpath, dirnames, filenames in os.walk(tmp_path):
    #     for dir in dirnames:
    #         if dir in metadata_file_names:

    #         os.makedirs(dir, exist_ok=True)


        # print(dirpath)
        # print(dirnames)
        # print(filenames)



    print(recovery_file)