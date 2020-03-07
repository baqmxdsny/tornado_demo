import logging
import tornado
import tornado.template
import os

from sqlalchemy.ext.declarative import declarative_base
from tornado.options import define, options
from sqlalchemy import create_engine
import cx_Oracle as orl
import environment
import logconfig

# Make filepaths relative to settings.
path = lambda root,*a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

define("port", default=8898, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")


tornado.options.parse_command_line()

MEDIA_ROOT = path(ROOT, 'media')
TEMPLATE_ROOT = path(ROOT, 'templates')

# Deployment Configuration

class DeploymentType:
    PRODUCTION = "PRODUCTION"
    DEV = "DEV"
    SOLO = "SOLO"
    STAGING = "STAGING"
    dict = {
        SOLO: 1,
        PRODUCTION: 2,
        DEV: 3,
        STAGING: 4
    }

if 'DEPLOYMENT_TYPE' in os.environ:
    DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
    DEPLOYMENT = DeploymentType.SOLO

settings = {}
settings['debug'] = DEPLOYMENT != DeploymentType.PRODUCTION or options.debug
settings['static_path'] = MEDIA_ROOT
settings['cookie_secret'] = "your-cookie-secret"
settings['xsrf_cookies'] = False
settings['template_loader'] = tornado.template.Loader(TEMPLATE_ROOT)

SYSLOG_TAG = "boilerplate"
SYSLOG_FACILITY = logging.handlers.SysLogHandler.LOG_LOCAL2

# See PEP 391 and logconfig for formatting help.  Each section of LOGGERS
# will get merged into the corresponding section of log_settings.py.
# Handlers and log levels are set up automatically based on LOG_LEVEL and DEBUG
# unless you set them here.  Messages will not propagate through a logger
# unless propagate: True is set.
LOGGERS = {
   'loggers': {
        'boilerplate': {},
    },
}

if settings['debug']:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO
USE_SYSLOG = DEPLOYMENT != DeploymentType.SOLO

logconfig.initialize_logging(SYSLOG_TAG, SYSLOG_FACILITY, LOGGERS,
        LOG_LEVEL, USE_SYSLOG)

if options.config:
    tornado.options.parse_config_file(options.config)


'''
    
    数据库连接

'''
system_order = "PRODUCTION"  # 生产环境变量名称

settings_files = os.environ.get(system_order)  # 获取系统环境变量PRODUCTION
settings_files = "productio"
if settings_files == "production":
    DEBUG = False  # 生产环境关闭DEBUG
else:
    DEBUG = True  # 开发环境

if settings_files == "production":  # 生产环境
    print('正式数据库！！！')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.oracle',
            'NAME': 'orcl',  # 数据库名称
            'USER': 'tdms',  # 用户名
            'PASSWORD': 'swd_2019_tdms1314',  # 密码
            'HOST': '172.30.201.21',  # HOST
            'PORT': '1521',  # 端口
            'charset': 'utf8'
        }
    }

else:  # 开发环境
    print('开发数据库')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.oracle',
            'NAME': 'orcl',  # 数据库名称
            'USER': 'tdms',  # 用户名
            'PASSWORD': 'swd2018tdms',  # 密码
            'HOST': '172.30.201.56',  # HOST
            'PORT': '1521',  # 端口
            'charset': 'utf8'
        }
    }

DB_URL = 'oracle+cx_oracle://{}:{}@{}:{}/?service_name={}'.format(
    DATABASES['default']['USER'],
    DATABASES['default']['PASSWORD'],
    DATABASES['default']['HOST'],
    DATABASES['default']['PORT'],
    DATABASES['default']['NAME']
)
ORL_URL = "{}/{}@{}:{}/{}".format(
    DATABASES['default']['USER'],
    DATABASES['default']['PASSWORD'],
    DATABASES['default']['HOST'],
    DATABASES['default']['PORT'],
    DATABASES['default']['NAME']
)
db_engine=create_engine(DB_URL, echo=True, max_overflow=5,implicit_returning=True)
db = orl.Connection(ORL_URL)
Base = declarative_base()
