import os
import sys

# add current directory to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import web

# check for testing env
def is_test():
    return os.getenv('WEBPY_ENV', '') == 'test'

# set web.py as in debug mode?
web.config.debug = (os.getenv('WEBPY_DEBUG', 0))

import mongoengine

# set mongodb config
MONGO_HOST = os.getenv('MONGODB_HOST', '127.0.0.1')
MONGO_PORT = os.getenv('MONGODB_PORT', 27017)
MONGO_DB = os.getenv('MONGODB_DB', 'traces')

# port may be passed in host with colon sep
if ':' in MONGO_HOST:
    (MONGO_HOST, MONGO_PORT) = MONGO_HOST.split(':')

db = mongoengine.connect(
    MONGO_DB, host=MONGO_HOST, port=int(MONGO_PORT)
)

thrift = dict({
    'host': os.getenv('THRIFT_HOST', '127.0.0.1'),
    'port': os.getenv('THRIFT_PORT', 6000),
    'rules': os.getenv('THRIFT_FILE', os.curdir + '/tracelogs.thrift'),
    'module': os.getenv('THRIFT_MODULE', 'tracelogs_thrift'),
    'service': 'TraceLogService',
})
