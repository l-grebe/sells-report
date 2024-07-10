import os
import argparse
from configparser import SectionProxy, RawConfigParser


class ProgramArgs:
    config: str
    entry_fn: str

    def __init__(self, args: argparse.Namespace):
        self.config = args.config
        self.entry_fn = args.entry_fn


class DefaultSetting:
    debug: bool
    host: str
    port: int

    def __init__(self, section: SectionProxy):
        self.debug = section.getboolean('debug')
        self.host = section.get('host')
        self.port = section.getint('port')


def get_config(config: str) -> RawConfigParser:
    filename = f'conf/{config}'
    cf = RawConfigParser()
    if os.path.isfile(filename):
        cf.read(filename, encoding="utf-8")
    else:
        raise IOError(filename + ' does not exist or not file.')
    return cf


_argp = argparse.ArgumentParser()
_argp.add_argument('--config', default='default.ini', type=str)
_argp.add_argument('--entry_fn', default='web', type=str)  # 入口函数

# _unknown_args: 未定义的参数
_args, _unknown_args = _argp.parse_known_args()

# 命令行参数
program_args = ProgramArgs(_args)

_cf = get_config(program_args.config)

# default配置
default_setting = DefaultSetting(_cf['default'])
