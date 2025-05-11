#!/usr/bin/python3.12
from conf_tools.restor_config import restor_config
from conf_tools.scan_config import scan_config
from setting.set_home import check_user_home, change_home
import os
import sys

    


def main():
    args = sys.argv[1:]

    home_dir = check_user_home()
    paths = change_home(home_dir)

    if len(args) == 0:
        exists_conf = [path for path in paths if os.path.exists(path)]
        scan_config(exists_conf)
    elif len(args) == 1:
        restor_config(args[0])   
    else:
        print()




if __name__ == "__main__":
    main()
