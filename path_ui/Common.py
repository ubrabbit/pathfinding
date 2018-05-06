#coding: utf-8

import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler

GridColorList=[
        "",
        "#aaaaff","#00aa7f",
        "#aa55ff","#555500","#55557f",
        "#00007f","#aa0000",
]
ColorEmpty=""
ColorEnter="#00aaff"
ColorExit="#00ff00"
ColorBlock="#000000"
ColorSearchPos="#aaffff"
SpecialColors=[ColorEnter,ColorExit,ColorBlock]

ColorEmptyIdx=GridColorList.index(ColorEmpty)

SizeSelectList=[10,20,50,80,100,200,]

DEFINE_REDIRECT_STDOUT = 1

VERSION=0.01


def log_file(sLog):
    global g_logger
    if not "g_logger" in globals():
        logFilePath = "%s/logfile.log"%(get_logpath())
        obj_log = logging.getLogger("logfile")
        obj_log.setLevel(logging.INFO)
        handler = TimedRotatingFileHandler(logFilePath,
                       when="d",
                       interval=1,
                       backupCount=7)
        obj_log.addHandler(handler)
        g_logger = obj_log

    time_info=time.strftime('%Y-%m-%d %H:%M:%S')
    sLog="[%s] %s"%(time_info,sLog)
    g_logger.info(sLog)
    return g_logger

def debug_print():
    import traceback
    traceback.print_exc()

def singleton_cls(cls, *args, **kw):
    instances = {}
    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

def recursion_make_dir(path, permit=0o755) :
    import os
    path = path.replace("\\","/")
    if os.path.exists(path) : return False
    os.makedirs(path)
    os.chmod(path, permit)
    return True

def init_runpath():
    cur_path = os.getcwd()
    obj_cfg = get_config_obj()
    obj_cfg.PROCESS_RUN_PATH = cur_path

    log_path = "%s/log"%cur_path
    data_path = "%s/data"%cur_path
    cache_path = "%s/cache"%cur_path

    recursion_make_dir( log_path )
    recursion_make_dir( data_path )
    recursion_make_dir( cache_path )

    obj_cfg.PROCESS_ROOT = cur_path
    obj_cfg.PROCESS_LOG_PATH = log_path
    obj_cfg.PROCESS_DATA_PATH = data_path
    obj_cfg.PROCESS_CACHE_PATH = cache_path

#全局对象，单例
@singleton_cls
class CGlobalConfig(object):

    pass

def get_config_obj():
    global g_global_config
    if not "g_global_config" in globals():
        global g_global_config
        g_global_config = CGlobalConfig()
        init_runpath()
    return g_global_config

def set_setting(attr, value):
    obj_cfg = get_config_obj()
    return setattr(obj_cfg, attr, value)

def get_setting(attr):
    obj_cfg = get_config_obj()
    return getattr(obj_cfg, attr)

def get_runpath():
    get_setting("PROCESS_RUN_PATH")

def get_datapath(*subdirs):
    dirpath = get_setting("PROCESS_DATA_PATH")
    if subdirs:
        dirpath = "%s/%s"%(dirpath, "/".join(subdirs))
        recursion_make_dir(dirpath)
        return dirpath
    return dirpath

def get_cachepath(*subdirs):
    dirpath = get_setting("PROCESS_CACHE_PATH")
    if subdirs:
        dirpath = "%s/%s"%(dirpath, "/".join(subdirs))
        recursion_make_dir(dirpath)
        return dirpath
    return dirpath

def get_logpath():
    return get_setting("PROCESS_LOG_PATH")
