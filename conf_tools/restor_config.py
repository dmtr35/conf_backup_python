import os
import json
import sys
from datetime import datetime
import tarfile






def restor_config(recovery_file):
    if not os.path.exists(recovery_file):
        return
    
    tmp_path = os.path.join("/tmp", recovery_file).removesuffix(".tar.gz")

    with tarfile.open(recovery_file, "r:gz") as tar:
        tar.extractall(path=tmp_path)
        print(f"файл распакован в {tmp_path}")

    metadata_path =os.path.join(tmp_path, "metadata.json")
    list_files = [os.path.join(tmp_path, f) for f in os.listdir(tmp_path) if f not in "metadata.json"]

    with open(metadata_path, 'r') as f:                                 # Загружаем конфигурацию из файла
        metadata_file = json.load(f)



    print(recovery_file)