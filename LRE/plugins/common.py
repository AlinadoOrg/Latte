#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os, sys
import threading
from .error import ConfigException, ReadConfigException



# This is a global configuration class,
# through which we can easily get configuration information
class AppConfig(object):
    # This is a thread lock and we will use it when getting the object instance.
    _INSTANCE_LOCK = threading.Lock()
    # This is a singleton object
    _INSTANCE = None
    # Get the class method of an instance of this class, which is a singleton
    @classmethod
    def instance(cls, *args, **kwargs):
        # By adding a thread lock,
        # we can make it still correct in the case of multithreading.
        with cls._INSTANCE_LOCK:
            # If it is None, create this instance
            if cls._INSTANCE is None:
                cls._INSTANCE = AppConfig(*args, **kwargs)
        # Return instance
        return cls._INSTANCE

    # The object's initialization method,
    # which will only be executed once because it is a singleton mode.
    # And read the configuration information of the Latte.json file during execution.
    def __init__(self):
        # Get the path to the LRE root directory
        # If there is no 'LATTEPATH' in the current system variable,
        # use the current program to run the directory
        lattepath = os.environ.get('LATTEPATH') if os.environ.get('LATTEPATH') else os.getcwd()
        # Get the path to the LRE plugin directory
        # If there is no 'LATTE_PLUGIN_PATH' in the current system variable,
        # use the path to the plugins folder under lattepath
        pluginpath = os.environ.get('LATTE_PLUGIN_PATH')
        if pluginpath:
            pluginpath = os.sep.join([lattepath, 'plugins'])
        # Get the path to the LRE config directory
        # If there is no 'LATTE_CONFIG_PATH' in the current system variable,
        # use the path to the config folder under lattepath
        configpath = os.environ.get('LATTE_CONFIG_PATH')
        if configpath:
            configpath = os.sep.join([lattepath, 'config'])
        # This is the default configuration information, it is comprehensive
        self.default = {
            # Latte system configuration information, which is not user-definable
            'sys': {
                'lattepath': lattepath,
                'configpath': configpath,
                'pluginpath': pluginpath
            }
        }
        # The log is temporarily stored here
        logTempStore = {
            'debug': [],
            'warn': []
        }
        # Get logger instance
        self.logger = Logger.getlogger(self.__class__.__name__)
        logTempStore['debug'].append('The current latte system environment variables are as follows:\n\tLATTEPATH: \'%s\',\n\tLATTE_CONFIG_PATH: \'%s\',\n\tLATTE_PLUGIN_PATH: \'%s\' ', lattepath, configpath, pluginpath)
        try:
            # Read the latte.json configuration file and throw if an exception occurs
            latteconfig = os.sep.join([configpath, 'latte.json'])
            if not os.path.isfile(latteconfig):
                raise ConfigException('Could not find the latte.json configuration file, or it is not a readable file.' + configpath)
            with open(latteconfig, 'r', encoding='utf-8') as config:
                self.userconfig = json.load(config)
            # Traverse all folders under the pluginpath and read the plugin.json configuration file
            self.plugins = {}
            for pluginname in os.listdir(pluginpath):
                latteplugin = os.sep.join([pluginpath, pluginname, 'plugin.json'])
                if not os.path.isfile(latteplugin):
                    # If there is no plugin.json file in the plugin directory,
                    # skip the plugin and output a warning log.
                    logTempStore['warn'].append('There is no plugin.json file under this plugin \'%s\'. ' % pluginname)
                    continue
                # Read the configuration file and save it to the 'plugins'
                with open(latteplugin, 'r', encoding='utf-8') as plugin:
                    self.plugins[pluginname] = json.load(plugin)
            logTempStore['debug'].append('The plugin that was successfully read into the configuration is as follows: [%s]', ', '.join(self.plugins.keys()))
        except UnicodeError as e:
            self.logger.exit(ConfigException('%s(%s)' % (e, 'make sure the configuration file is UTF-8 encoded.')))
        except ConfigException as e:
            self.logger.exit(e)
        except Exception as e:
            self.logger.exit(ConfigException(e))
        #

    # This is a way to get plugin configuration information using a key such as "multi.level.key".
    def get_plugin_config(self, k):
        # Throws an exception if k is not a string
        if not isinstance(k, str):
            raise ReadConfigException('The key [' + str(k) + '] not is str type')
        # Split k with '.'
        keys = k.split('.')
        # Get the length of the keys array
        keylength = len(keys)
        # plugins as root
        root = self.plugins
        # Traverse plugin configuration
        for i in range(0, keylength):
            key = keys[i]
            # If root is not a list or dict or tuple,
            # Or the key is not in a user-defined configuration, then the loop is exited
            if (type(root) not in [list, dict, tuple]) or (key not in root):
                break
            # If this is the last key, the value corresponding to this key is returned.
            if i == keylength - 1:
                return root[key]
            # If neither of the above is true,
            # assign the value of 'root[key]' to 'root' and continue traversing
            root = root[key]
        # Oh, when I got here, it must be because I didn’t find 'k'.
        # So we should throw a ReadConfigException here.
        raise ReadConfigException('No such key: \'%s\'.' % k)

def initializa():
    # Use the Logs folder in the run directory as the default log output folder
    default_log_output_path = os.sep.join([os.getcwd(), 'logs'])
    # Set the log default output path
    # This will cause all logs to be output to the same location
    Logger._LogOutputPath['all'] = default_log_output_path
    Logger._LogOutputPath['debug'] = default_log_output_path
    Logger._LogOutputPath['info'] = default_log_output_path
    Logger._LogOutputPath['warning'] = default_log_output_path
    Logger._LogOutputPath['error'] = default_log_output_path
    Logger._LogOutputPath['critical'] = default_log_output_path
    # Initialize AppConfig
    appConfig = AppConfig.instance()
