#!/usr/bin/env python
# coding: utf-8

import sys
import web

import config

from modules.log import logger

urls = (
    "/traces", "modules.controller.TracesHTTPController"
)

app = web.application(urls, globals())

def error_handler(handler):
    try:
        handler()

    except web.HTTPError as exhttp:
        logger.debug('HTTP return status: %s' % exhttp)
        raise exhttp

    except Exception as ex:
        logger.error('Application error: %s' % ex)
        raise web.internalerror()

app.add_processor(error_handler)

try:
    if __name__ == "__main__":
        app.run()
    else:
        webapp = app.wsgifunc()

except KeyboardInterrupt:
    logger.info("Exiting by user SIGINT (Ctrl+C)")
    sys.exit()
