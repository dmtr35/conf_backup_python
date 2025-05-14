#!/usr/bin/python3.12
from tools.restor_config import restor_config
from tools.scan_config import scan_config
import os
import sys

    


def main():
    args = sys.argv[1:]
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_dir, "config.json")

    if len(args) == 0:
        scan_config(config_path)
    elif len(args) == 1:
        restor_config(args[0])   
    else:
        print()

if __name__ == "__main__":
    main()
