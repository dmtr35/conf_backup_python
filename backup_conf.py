#!/usr/bin/python3.12
from conf_tools.restor_config import restor_config
from conf_tools.scan_config import scan_config
from setting.set_home import check_user_home, change_home
import os
import sys

    


def main():
    home_dir = check_user_home()
    paths = change_home(home_dir)

    if len(sys.argv) == 1:
        exists_conf = [path for path in paths if os.path.exists(path)]
        print(exists_conf)
        print("\n")
        scan_config(exists_conf)
    else:
        restor_config(paths)   





if __name__ == "__main__":
    main()
