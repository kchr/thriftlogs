#!/usr/bin/env python
# coding: utf-8

import sys
import argparse

import config


def parse():

    parser = argparse.ArgumentParser(
        description='External client for TraceLogService')

    parser.add_argument('-s', help='thrift server hostname', metavar='HOSTNAME',
                        type=str, dest='thrift_server',
                        default=config.thrift.get('host'))

    parser.add_argument('-p', help='thrift server port', metavar='PORT',
                        type=str, dest='thrift_port',
                        default=config.thrift.get('port'))

    parser.add_argument('--verbose', help='show extra details',
                        dest='verbose', action='store_true', default=False)

    subparsers = parser.add_subparsers(title='subcommands',
                                       description='RPC methods',
                                       dest='command')

    bucket_parser = subparsers.add_parser('createBucket',
                                          help='create new bucket')

    bucket_parser.add_argument('name', metavar='NAME', type=str,
                               help='name of bucket (required)')

    traces_parser = subparsers.add_parser('getTraces',
                                          help='get all traces in a bucket')

    traces_parser.add_argument('token', metavar='TOKEN', type=str,
                               help='bucket token (required)')

    traces_parser.add_argument('--type', metavar='ERROR_TYPE', type=str,
                               help='type of error', dest='error_type')

    args = parser.parse_args()

    return args
