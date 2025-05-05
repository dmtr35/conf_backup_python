import os
import pwd
import json

def check_user_home():
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        home_dir = pwd.getpwnam(sudo_user).pw_dir
    else:
        home_dir = os.environ.get("HOME")
    return home_dir


def change_home(home_dir):
    orig_home = os.environ["HOME"]
    try:
        os.environ["HOME"] = home_dir                                       # Временно устанавливаем HOME в значение home_dir
        with open('config.json', 'r') as f:                                 # Загружаем конфигурацию из файла
            config = json.load(f)
        paths = [os.path.expanduser(os.path.expandvars(p)) for p in config['config_paths']]
    finally:
        if orig_home is not None:
            os.environ["HOME"] = orig_home                                  # Восстанавливаем HOME
        else:
            os.environ.pop("HOME", None)
    return paths
