from setting.set_data import save_system_info, collect_metadata
import os
import shutil
import json
import tarfile
from datetime import datetime




def scan_config(paths: list):
    now = datetime.now()
    date_string = now.strftime("_%d.%m.%Y_%H-%M")
    tmp_folder = "/tmp/conf_backup" + date_string
    metadata_file = os.path.join(tmp_folder, "metadata.json")
    os.makedirs(tmp_folder, exist_ok=True)

    host_name = save_system_info(tmp_folder)

    metadata = {}
    for src_path in paths:
        dest_base = os.path.join(tmp_folder, os.path.basename(src_path))
        if os.path.isdir(src_path):
            collect_metadata(src_path, metadata)
            for dirpath, dirnames, filenames in os.walk(src_path):
                rel_path = os.path.relpath(dirpath, src_path)
                dest_path = os.path.join(dest_base, rel_path)
                os.makedirs(dest_path, exist_ok=True)

                # Сохраняем метаданные для директорий
                for dir in dirnames:
                    src_dir = os.path.join(dirpath, dir)
                    collect_metadata(src_dir, metadata)

                # Копируем файлы
                for filename in filenames:
                    src_file = os.path.join(dirpath, filename)
                    if not os.path.isfile(src_file):
                        continue
                    collect_metadata(src_file, metadata)
                    dest_file = os.path.join(dest_path, filename)
                    shutil.copy2(src_file, dest_file)
        else:
            if os.path.isfile(src_path):
                collect_metadata(src_path, metadata)
                shutil.copy2(src_path, dest_base)

    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)

    folder_name = os.path.basename(tmp_folder)
    backup_file_path = os.path.join(".", f"{folder_name}_{host_name}.tar.gz")

    with tarfile.open(backup_file_path, "w:gz") as tar:
        tar.add(tmp_folder, arcname=folder_name)

    shutil.rmtree(tmp_folder)

