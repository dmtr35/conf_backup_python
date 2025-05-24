from tools.restore_config import restore_config
from tools.scan_config import scan_config
from setting.check_permission import check_permission
import os
import sys


def main():
    check_permission()

    args = sys.argv[1:]
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_dir, "config.json")
    save_original = 0

    if "-h" in args or "--help" in args:
        print("""
./ConfBackup                        - делать backup файлов из списка config.json[config_paths]
./ConfBackup -s file-backup         - сохранять оригинальные файлы с приставкой .bak перед восстановлением
./ConfBackup file-backup            - если config.json[restore_list] не пустой, делать восстановление из этого списка
""")
        return
    
    if "-s" in args:
        args.remove("-s")
        save_original = 1


    if len(args) == 0:
        scan_config(config_path, script_dir)
    else:
        restore_config(args[0], config_path, save_original)   

if __name__ == "__main__":
    main()
