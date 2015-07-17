#!/usr/bin/env python
# coding: utf-8

import config

from modules.log import logsetup, logger

from socket import error as socket_error

import thriftpy

from thriftpy.protocol import TCyBinaryProtocolFactory
from thriftpy.transport import TCyBufferedTransportFactory

from thriftpy.rpc import make_server

from modules.controller import TracesThriftServerController

tracelogs_thrift = thriftpy.load(config.thrift.get('rules'),
                                 module_name=config.thrift.get('module'))


def do_serve(host, port):

    print "Starting thrift server on %s:%s..." % (host, port)

    try:
        server = make_server(
            tracelogs_thrift.TraceLogService,
            TracesThriftServerController(module=tracelogs_thrift),
            host, port,
            proto_factory=TCyBinaryProtocolFactory(),
            trans_factory=TCyBufferedTransportFactory()
        )

        server.serve()

    except thriftpy.thrift.TException as ex:
        logger.error('Thrift error: %s' % ex.message)

    except socket_error as sex:
        logger.error('Network error: %s' % sex)

    except Exception as ex:
        logger.error('Application error: %s' % ex)
        raise

if __name__ == '__main__':

    logsetup()

    do_serve(config.thrift.get('host'),
             config.thrift.get('port'))
