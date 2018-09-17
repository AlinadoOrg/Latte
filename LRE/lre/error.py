#!/usr/bin/env python
# -*- coding: utf-8 -*-
class LatteException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class LatteRuntimeError(LatteException, RuntimeError):
    def __init__(self, *args, **kwargs):
        RuntimeError.__init__(*args, **kwargs)

class ConfigException(LatteException, OSError):
    def __init__(self, msg):
        err = 'Incorrect configuration file: %s' % msg
        OSError.__init__(self, err)

class ReadConfigException(LatteRuntimeError, ConfigException, IOError):
    def __init__(self, msg):
        err = 'Cannot read configuration: %s' % msg
        RuntimeError.__init__(self, err)
