#!/usr/bin/env python
# coding: utf-8
import config

from modules.client import parse
from modules.log import logsetup, logger

import thriftpy

tracelogs_thrift = thriftpy.load(config.thrift.get('rules'),
                                 module_name=config.thrift.get('module'))

from thriftpy.rpc import client_context

from thriftpy.protocol import TCyBinaryProtocolFactory
from thriftpy.transport import TCyBufferedTransportFactory

from modules.controller import TracesThriftClientController

from socket import error as socket_error


def main():

    args = parse()
    args_dict = dict(args.__dict__)

    logsetup(args_dict)

    try:

        # create thrift client
        with client_context(tracelogs_thrift.TraceLogService,
                            config.thrift.get('host'),
                            config.thrift.get('port'),
                            proto_factory=TCyBinaryProtocolFactory(),
                            trans_factory=TCyBufferedTransportFactory()
                            ) as thrift_client:

            client = TracesThriftClientController(client=thrift_client,
                                                  module=tracelogs_thrift)

            output = client.dispatchCall(args.command, args)

            print output


    except thriftpy.thrift.TException as ex:
        logger.error('Thrift error: %s' % ex.message)

    except socket_error as sex:
        logger.error('Network error: %s' % sex)

    except Exception as ex:
        logger.error('Application error: %s' % ex)
        raise

if __name__ == '__main__':

    main()
