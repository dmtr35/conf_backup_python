import os
import sys


def check_permission():
    if os.geteuid() != 0:
        print("This script must be run as root!")
        # sys.exit(1)                                 # Exit with error
    else:
        print("Running as root.")