import os

from configparser import ConfigParser

from utils.aux import lazyparse

main_cfg_file = './config/main.cfg'

if not os.path.exists(main_cfg_file):
    raise FileNotFoundError('Cannot find configuration file at {}'.format(main_cfg_file))


# todo: wrap this nonsense
def load_cfg():
    cfg = ConfigParser()
    cfg.read(main_cfg_file)
    d = {sec: dict(cfg[sec]) for sec in cfg}
    return d

def load_cfg_section(sec):
    cfg = ConfigParser()
    cfg.read(main_cfg_file)
    return dict(cfg[sec])


def get_cfg_param(sec, param=None):
    # sec, param = namespace.split('.')
    cfgsec = load_cfg_section(sec)
    if param is not None:
        return lazyparse(cfgsec[param])

