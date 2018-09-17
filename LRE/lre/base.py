#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io, os, sys, json
import traceback
import logging
from logging.handlers import TimedRotatingFileHandler
from .error import ConfigException, ReadConfigException

# 日志基类
# Logger base class
class Logger(object):
    # 日志配置信息
    # Log configuration information
    __Uninitialized = True
    # 初始化日志配置
    # Initialize log configuration
    @classmethod
    def init(cls):
        # 确认它是否已初始化
        # Determine if it has been initialized
        if cls.__Uninitialized:
            # 尝试获取记录器配置文件
            # Try to get the logger configuration file
            configFile = LatteConfig.findConfig('logger.config')
            if configFile is not None:
                # 如果有日志配置文件，请直接从该文件构造Logger
                # If there is a log configuration file, construct a Logger directly from the file
                path = configFile
                # 如果configFile不是绝对路径，
                # 它被视为相对于lattepath的相对路径
                # If configFile is not an absolute path,
                # it is treated as a relative path relative to lattepath
                if configFile[0] != '/':
                    path = os.sep.join([LatteConfig['sys.path.latte'], configFile])
                # 读取configFile以构建记录器
                # Read configFile to construct the logger
                logging.config.fileConfig(path, disable_existing_loggers=True)
                # 声明已初始化
                # The declaration has been initialized
                cls.__Uninitialized = False
            else:
                # 读取日志配置信息
                # Read log configuration information
                # 获取日志输出目录
                # Get the log output directory
                loggerPath = LatteConfig.getConfig('logger.path')
                # 验证日志文件夹是否存在
                # Verify that the log folder exists
                if not os.path.exists(loggerPath):
                    # 创建日志文件夹
                    # Create a log folder
                    os.makedirs(loggerPath)
                elif not os.path.isdir(loggerPath):
                    cls.exit('Unable to create log folder')

                # 获取日志等级
                # Get log level
                level = LatteConfig.getConfig('logger.level').lower()
                # 确定日志级别并获得正确的等级
                # Determine the log level and get the correct rating
                if level == 'debug':
                    level = logging.DEBUG
                elif level == 'info':
                    level = logging.INFO
                elif level == 'error':
                    level = logging.ERROR
                elif level == 'critical':
                    level = logging.CRITICAL
                else:
                    # 当级别不在规范范围内时，
                    # 它被视为Warning级别。
                    # When the level is not within the scope of the specification,
                    # it is treated as the Warning level.
                    level = logging.WARNING
                # 获取日志输出格式
                # Get log output format
                format = LatteConfig.getConfig('logger.format')
                # 获取日志日期时间格式
                # Get log datetime format
                datefmt = LatteConfig.getConfig('logger.datefmt')
                # 获取日志输出文件名
                # Get log file output name
                filename = LatteConfig.getConfig('logger.file.filename')
                # 获取日志文件拆分间隔
                # Get log file split interval
                when = LatteConfig.getConfig('logger.file.when')
                # 获取日志文件名后缀
                # Get the log file name suffix
                suffix = LatteConfig.getConfig('logger.file.suffix')
                # 获取日志间隔
                # Get log interval
                interval = LatteConfig.getConfig('logger.file.interval')
                # 获取日志备份数量
                # Get log backups count
                backupCount = LatteConfig.getConfig('logger.file.backupCount')
                # 构建日志输出路径
                # Build log output path
                outpath = os.sep.join([loggerPath, filename])
                # 写入日志基本配置信息
                # 这将默认创建控制台输出。
                # Write log basic configuration
                # This will create the console output by default.
                logging.basicConfig(level=level, format=format, datefmt=datefmt)
                # 创建日志Formatter对象
                # Create a log formatting object
                formatter = logging.Formatter(format, datefmt)
                # 创建日志输出Handler对象
                # Create a file output Handler
                handler = TimedRotatingFileHandler(outpath, when, interval, backupCount)
                handler.setFormatter(formatter)
                # 设置记录日志等级
                # Set the logging level
                handler.setLevel(level)
                # 写入文件前缀风格
                # Write file suffix style
                handler.suffix = suffix
                # 将文件输出Handler注册到全局Logger中
                # Register the file output Handler into the global Logger
                logging.getLogger().addHandler(handler)
                # 声明已初始化
                # The declaration has been initialized
                cls.__Uninitialized = False

    # 退出程序
    # 如果指定了异常，
    # 将打印一个异常，程序将意外退出。
    # exit the program
    # If an exception is specified,
    # an exception will be printed and the program will exit unexpectedly.
    @classmethod
    def exit(cls, e=None):
        if e is not None:
            # 如果指定了异常对象，
            # 将首先记录日志并退出日志
            # If an exception object is specified,
            # the log will be logged first and exited
            try:
                # 如果日志尚未初始化，
                # 将使用默认录制方法。
                # If the log has not been initialized,
                # the default recording method will be used.
                if cls.__Uninitialized:
                    # 打印到控制台
                    # Print to console
                    traceback.print_exc()
                    # 记录到文件
                    # Record to file
                    traceback.print_exc(file=open(os.sep.join([os.getcwd(), 'latte-error.log']), 'a'))
                else:
                    # 如果已初始化，则会将其记录到日志目录中。
                    # If it has been initialized, it will be logged to the log directory.
                    logger = cls.getLogger('latte')
                    logger.exception(e)
            finally:
                # 程序意外退出
                # The program quits unexpectedly
                sys.exit(1)
        # 如果未指定异常对象，程序将正常退出。
        # If no exception object is specified, the program will exit normally.
        sys.exit(0)

    # 获取Logger对象
    # Get Logger
    @classmethod
    def getLogger(cls, app='root'):
        # 确认它是否已初始化
        # Determine if it has been initialized
        if cls.__Uninitialized:
            cls.init()
        return logging.getLogger(app)

    # 记录日志
    # Record logs
    @classmethod
    def log(cls, *args, **kwargs):
        cls.getLogger().log(*args, **kwargs)

    # 记录 DEBUG 级别日志
    # Record DEBUG level logs
    @classmethod
    def debug(cls, *args, **kwargs):
        cls.getLogger().debug(*args, **kwargs)

    # 记录 INFO 级别日志
    # Record INFO level logs
    @classmethod
    def info(cls, *args, **kwargs):
        cls.getLogger().info(*args, **kwargs)

    # 记录 WARNING 级别日志
    # Record WARNING level logs
    @classmethod
    def warn(cls, *args, **kwargs):
        cls.getLogger().warning(*args, **kwargs)

    # 记录 WARNING 级别日志
    # Record WARNING level logs
    @classmethod
    def warning(cls, *args, **kwargs):
        cls.getLogger().warning(*args, **kwargs)

    # 记录 ERROR 级别日志
    # Record ERROR level logs
    @classmethod
    def error(cls, *args, **kwargs):
        cls.getLogger().error(*args, **kwargs)

    # 记录 CRITICAL 级别日志
    # Record CRITICAL level logs
    @classmethod
    def critical(cls, *args, **kwargs):
        cls.getLogger().critical(*args, **kwargs)

    # 记录异常日志
    # Record exception log
    @classmethod
    def exception(cls, *args, **kwargs):
        cls.getLogger().exception(*args, **kwargs)


# Latte基本配置信息类
# Latte basic configuration information class
class LatteConfig(object):
    # 这是用户配置信息，在启动时加载
    # This is the user configuration information, which is loaded at startup.
    __UserConfig = None
    # 这是默认的配置信息，它是非常完善的
    # This is the default configuration information, it is comprehensive
    __DefaultConfig = {
        'logger': {
            'path': os.getcwd(),
            'level': 'DEBUG',
            'format': '[%(levelname)-8s] %(asctime)s %(threadName)s %(name)s.%(module)s(%(lineno)d): \n\t%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'file': {
                'filename': 'latte.log',
                'when': 'D',
                'suffix': '%Y%m%d.log',
                'interval': 1,
                'backupCount': 7
            }
        },
        'robot': {
            'name': 'Latte'
        }
    }
    # 初始化latte的基本配置信息
    # Initialize the basic configuration information of the latte
    @classmethod
    def init(cls):
        # ___UserConfig为None时执行初始化
        # 这意味着它只会被执行一次
        # Initialization is performed when __UserConfig is None
        # This means it will be executed only once
        if cls.__UserConfig is None:
            # 获取LRE根目录的路径
            # 如果当前系统变量中没有'LATTEPATH'，
            # 使用当前程序运行目录
            # Get the path to the LRE root directory
            # If there is no 'LATTEPATH' in the current system variable,
            # use the current program to run the directory
            lattePath = os.environ.get('LATTEPATH') if os.environ.get('LATTEPATH') else os.getcwd()
            # 获取LRE插件目录的路径
            # 如果当前系统变量中没有'LATTE_PLUGIN_PATH'，
            # 使用lattepath下的plugins文件夹的路径
            # Get the path to the LRE plugin directory
            # If there is no 'LATTE_PLUGIN_PATH' in the current system variable,
            # use the path to the plugins folder under lattepath
            pluginPath = os.environ.get('LATTE_PLUGIN_PATH')
            if not pluginPath:
                pluginPath = os.sep.join([lattePath, 'plugins'])
            # 获取LRE配置目录的路径
            # 如果当前系统变量中没有'LATTE_CONFIG_PATH'，
            # 使用lattepath下config文件夹的路径
            # Get the path to the LRE config directory
            # If there is no 'LATTE_CONFIG_PATH' in the current system variable,
            # use the path to the config folder under lattepath
            configPath = os.environ.get('LATTE_CONFIG_PATH')
            if not configPath:
                configPath = os.sep.join([lattePath, 'config'])
            # Latte系统配置信息，不是用户可定义的
            # Latte system configuration information, which is not user-definable
            sysConfig = {
                'sys': {
                    'path': {
                        'latte': lattePath,
                        'config': configPath,
                        'plugin': pluginPath
                    },
                }
            }
            # 更新cls.__DefaultConfig中的这些系统配置信息
            # Update these system configuration information in cls.__DefaultConfig
            cls.__DefaultConfig.update(sysConfig)
            # 更改默认日志的路径
            # Change the path of the default log
            cls.__DefaultConfig['logger']['path'] = os.sep.join([lattePath, 'logs'])
            try:
                # 在configpath下查找latte.json配置文件
                # Look for the latte.json configuration file under configpath
                latteconfig = os.sep.join([configPath, 'latte.json'])
                if not os.path.isfile(latteconfig):
                    raise ConfigException('Could not find the latte.json configuration file, or it is not a readable file.' + configpath)
                # 读取latte.json配置文件，如果发生异常则抛出
                # Read the latte.json configuration file and throw if an exception occurs
                with io.open(latteconfig, mode='r', encoding='utf-8') as config:
                    cls.__UserConfig = json.load(config)
            except Exception as e:
                # 拦截异常并退出程序
                # Intercept the exception and exit the program
                Logger.exit(e)

    # 内部定义私有函数
    # 遍历配置信息字典的功能
    # Internally defines a private function
    # that traverses the function of the configuration information dictionary
    @classmethod
    def __find(cls, keys, root):
        # 获取keys数组的长度
        # Get the length of the keys array
        length = len(keys)
        # 遍历配置信息
        # Traverse configuration
        for i in range(0, length):
            key = keys[i]
            # 如果root不是list或dict或tuple，
            # 或者key不在root中，则退出循环
            # If root is not a list or dict or tuple,
            # Or the key is not in root, then the loop is exited
            if (type(root) not in [list, dict, tuple]) or (key not in root):
                break
            # 如果这是最后一个key，则返回与该key对应的值。
            # If this is the last key, the value corresponding to this key is returned.
            if i == length - 1:
                return root[key]
            # 如果上述两者都不成立，
            # 则将'root[key]'的值赋给'root'并继续遍历
            # If neither of the above is true,
            # assign the value of 'root[key]' to 'root' and continue traversing
            root = root[key]

    # 使用诸如“the.multi.level.key”之类的key获取配置信息的值
    # Get the value of the configuration information using a key such as "the.multi.level.key"
    @classmethod
    def getConfig(cls, k):
        # 声明result
        # Statement result
        result = None
        # 验证初始化
        # Verify initialization
        if cls.__UserConfig is None:
            cls.init()
        # 如果k不是字符串，则抛出异常
        # Throws an exception if k is not a string
        if not isinstance(k, str):
            raise ReadConfigException('The key [' + str(k) + '] not is str type')
        # 用'.'拆分k
        # Split k with '.'
        keys = k.split('.')

        # 如果第一个是'sys'，则跳过用户配置信息
        # Skip user configuration information if the first is 'sys'
        if keys[0] != 'sys':
            # 使用用户配置信息作为根，
            # 遍历字典，找到k的值
            # Use the user configuration information as the root,
            # traverse the dictionary, and find the key value.
            result = cls.__find(keys, cls.__UserConfig)

        # 指定的密钥不在用户定义的配置中,
        # 因此，开始遍历默认配置
        # The specified key is not in the user-defined configuration
        # So, start traversing the default configuration
        result = cls.__find(keys, cls.__DefaultConfig)

        # 当result不是None时返回结果
        # Return the result when it is not None
        if result is not None:
            return result
        # 哦，当我到达这里时，一定是因为我找不到'k'.
        # 所以我们应该在这里抛出一个ReadConfigException异常.
        # Oh, when I got here, it must be because I didn’t find 'k'.
        # So we should throw a ReadConfigException here.
        raise ReadConfigException('No such key: \'%s\'.' % k)

    # 使用诸如“the.multi.level.key”之类的key获取配置信息的值
    # 如果指定的配置不存在，则返回default
    # Get the value of the configuration information using a key such as "the.multi.level.key"
    # Returns the default value if the specified configuration does not exist
    @classmethod
    def getConfigOrDefault(cls, k, default):
        # 捕获异常
        # Capture exception
        try:
            return cls.getConfig(k)
        # 它只会尝试捕获ReadConfigException,
        # 不管其他异常
        # It will only try to catch a ReadConfigException,
        # regardless of other exceptions.
        except ReadConfigException:
            return default

    # 尝试获取配置信息，如果没有，则返回None
    # Try to get the configuration information, if not, return None
    @classmethod
    def findConfig(cls, k):
        try:
            return cls.getConfig(k)
        # 这将导致它拦截几乎所有异常并返回None
        # This will cause it to intercept almost all exceptions and return None
        except Exception:
            return None


class PluginConfig(object):
    __Names = []
    __Config = None
    # 初始化插件配置信息
    # Initialize plugin configuration information
    @classmethod
    def init(cls):
        # 只有在当cls.__Config不为None时，才会执行
        # Execute only when cls.__Config is not None
        if cls.__Config is None:
            cls.__Config = {}
            # 获取Logger对象
            # Get Logger object
            logger = Logger.getLogger('Latte.plugin')
            # 获取插件目录的路径
            # Get the path to the plugin directory
            pluginPath = LatteConfig.getConfig('sys.path.plugin')
            # 如果插件目录不是一个文件夹，则抛出异常
            # Throw an exception if the plugin directory is not a folder
            if not os.path.isdir(pluginPath):
                raise ConfigException('The specified plugin path does not exist or is not a folder')
            # 遍历插件目录下的每一个文件
            # Traverse every file in the plugin directory
            for name in os.listdir(pluginPath):
                # 拼接路径，得到当前遍历的插件的完整路径
                # Splicing path, get the full path of the currently traversed plugin
                currPluginPath = os.sep.join([pluginPath, name])
                # 如果这个文件不是一个文件夹，则跳过该插件，并且发出警告
                # If this file is not a folder, skip the plugin and issue a warning
                if not os.path.isdir(currPluginPath):
                    logger.warn('[Plugin \'%s\' is not loaded] File \'%s\' is not a folder.' % (name, name))
                    continue
                # 拼接路径，得到当前遍历的插件的配置文件的完整路径
                # Splicing path, get the full path of the configuration file of the currently traversed plugin
                pluginconfig = os.sep.join([currPluginPath, 'plugin.json'])
                # 如果这个配置文件不存在，或者不是文件，则跳过该插件，并且发出警告
                # If the configuration file does not exist or is not a file, skip the plugin and issue a warning
                if not os.path.isfile(pluginconfig):
                    logger.warn('[Plugin \'%s\' is not loaded] The plugin configuration file plugin.json is not found.' % name)
                    continue
                try:
                    # 读取插件的配置信息，并以插件名为Key，将它存入cls.__Config中
                    # Read the configuration information of the plugin and store it in cls.__Config with the plugin name Key.
                    with io.open(pluginconfig, mode='r', encoding='utf-8') as plugin:
                        cls.__Config[name] = json.load(plugin)
                        # 读取成功时，才会将插件名添加到名称域中
                        # The plugin name will be added to the name field when the read is successful
                        cls.__Names.append(name)
                except Exception as e:
                    # 如果读取配置时，发生任何异常，则跳过该插件，并发出警告
                    # If any exception occurs while reading the configuration, skip the plugin and issue a warning
                    logger.warn('[Plugin \'%s\' is not loaded] %s' % (name, e))
            # 如果cls.__Config内至少有一个元素，则执行下一步代码
            # If there is at least one element in cls.__Config, execute the next code
            # if cls.__Config:

    # 内部定义私有函数
    # 遍历配置信息字典的功能
    # Internally defines a private function
    # that traverses the function of the configuration information dictionary
    @classmethod
    def __find(cls, keys, root):
        # 获取keys数组的长度
        # Get the length of the keys array
        length = len(keys)
        # 遍历配置信息
        # Traverse configuration
        for i in range(0, length):
            key = keys[i]
            # 如果root不是list或dict或tuple，
            # 或者key不在root中，则退出循环
            # If root is not a list or dict or tuple,
            # Or the key is not in root, then the loop is exited
            if (type(root) not in [list, dict, tuple]) or (key not in root):
                break
            # 如果这是最后一个key，则返回与该key对应的值。
            # If this is the last key, the value corresponding to this key is returned.
            if i == length - 1:
                return root[key]
            # 如果上述两者都不成立，
            # 则将'root[key]'的值赋给'root'并继续遍历
            # If neither of the above is true,
            # assign the value of 'root[key]' to 'root' and continue traversing
            root = root[key]

    # 获取全部的插件名称
    # Get all plugin names
    @classmethod
    def names(cls):
        return cls.__Names[:]

    # 使用诸如“the.multi.level.key”之类的key获取配置信息的值
    # Get the value of the configuration information using a key such as "the.multi.level.key"
    @classmethod
    def getConfig(cls, k):
        # 声明result
        # Statement result
        result = None
        # 验证初始化
        # Verify initialization
        if cls.__Config is None:
            cls.init()
        # 如果k不是字符串，则抛出异常
        # Throws an exception if k is not a string
        if not isinstance(k, str):
            raise ReadConfigException('The key [' + str(k) + '] not is str type')

        # 用'.'拆分k
        # Split k with '.'
        keys = k.split('.')

        # 遍历字典，找到k的值
        # traverse the dictionary, and find the key value.
        result = cls.__find(keys, cls.__Config)

        # 当result不是None时返回结果
        # Return the result when it is not None
        if result is not None:
            return result
        # 哦，当我到达这里时，一定是因为我找不到'k'.
        # 所以我们应该在这里抛出一个ReadConfigException异常.
        # Oh, when I got here, it must be because I didn’t find 'k'.
        # So we should throw a ReadConfigException here.
        raise ReadConfigException('No such key: \'%s\'.' % k)

    # 使用诸如“the.multi.level.key”之类的key获取配置信息的值
    # 如果指定的配置不存在，则返回default
    # Get the value of the configuration information using a key such as "the.multi.level.key"
    # Returns the default value if the specified configuration does not exist
    @classmethod
    def getConfigOrDefault(cls, k, default):
        # 捕获异常
        # Capture exception
        try:
            return cls.getConfig(k)
        # 它只会尝试捕获ReadConfigException,
        # 不管其他异常
        # It will only try to catch a ReadConfigException,
        # regardless of other exceptions.
        except ReadConfigException:
            return default

    # 尝试获取配置信息，如果没有，则返回None
    # Try to get the configuration information, if not, return None
    @classmethod
    def findConfig(cls, k):
        try:
            return cls.getConfig(k)
        # 这将导致它拦截几乎所有异常并返回None
        # This will cause it to intercept almost all exceptions and return None
        except Exception:
            return None

# 加载包时初始化Logger，LatteCofing和PluginConfig
# Initialize Logger, LatteCofing, and PluginConfig when the package is loaded
LatteConfig.init()
Logger.init()
PluginConfig.init()
