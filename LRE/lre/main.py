
from .base import PluginConfig, Logger

PLUGINS = []

def init():


def run():
    Logger.info('start latte')
    print(PluginConfig.names())
