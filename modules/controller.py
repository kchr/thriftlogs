#!/usr/bin/env python
# coding: utf-8

import re
import web
import json

import thriftpy

from handlers.traces import TracesHandler

from modules.log import logger


class TracesController(object):

    logger = None
    handler = None

    def __init__(self):
        self.logger = logger
        self.handler = TracesHandler()


class TracesThriftController(TracesController):

    __thrift = {
        'client': None,
        'module': None,
        'server': None
    }

    def __init__(self, *args, **kwargs):

        super(TracesThriftController, self).__init__()

        t_client = kwargs.get('client', None)
        t_module = kwargs.get('module', None)
        t_server = kwargs.get('server', None)

        if t_client and not isinstance(t_client, thriftpy.thrift.TClient):
            raise TypeError(
                'client should be an instance of thriftpy.thrift.TClient')

        self.__thrift.update({'client': t_client,
                              'module': t_module,
                              'server': t_server})

    def get_thrift(self, which='client'):
        return self.__thrift.get(which)

    def thrift_client(self):
        return self.get_thrift('client')

    def thrift_module(self):
        return self.get_thrift('module')


class TracesThriftServerController(TracesThriftController):
    ''' Controller for Thrift Server '''

    def __init__(self, *args, **kwargs):
        super(TracesThriftServerController, self).__init__(*args, **kwargs)

    def createBucket(self, request):
        """ @return CreateBucketResponse """

        tracelogs_thrift = self.thrift_module()

        response = tracelogs_thrift.CreateBucketResponse()

        try:
            bucket = self.handler.create_bucket(request.name)
            response.token = bucket.get_token()

        except Exception as ex:
            self.logger.error('createBucket(): %s' % ex)

        return response

    def getTraces(self, request):
        """ @return GetTracesResponse """

        tracelogs_thrift = self.thrift_module()

        response = tracelogs_thrift.GetTracesResponse()
        response.traces = []

        try:
            token = request.token
            bucket = self.handler.get_bucket(token)

            error_type = request.type or None

            traces = self.handler.get_list(bucket.get_token(), error_type)

            for tracedata in traces:

                t = tracelogs_thrift.Trace()

                t.type = tracedata.type
                t.message = tracedata.message
                t.stack = tracedata.stack
                t.context = tracedata.context

                response.traces.append(t)

        except Exception as ex:
            self.logger.error('getTraces(): %s' % ex)

        return response

class TracesThriftClientController(TracesThriftController):
    ''' Controller for CLI client usage of TracesHandler '''

    def __init__(self, *args, **kwargs):
        super(TracesThriftClientController, self).__init__(*args, **kwargs)

    """
    Verify target method exists in thrift client specification

        @required string name
    """
    def __verify_method(self, name):
        try:
            getattr(self.thrift_client(), name)
        except AttributeError:
            raise Exception('Method does not exist: %s' % name)

    """
    Route client request to local proxy method

        @required string name
        @required argparse.Namespace args
    """
    def dispatchCall(self, name, args):

        try:
            # make sure target method exists in thrift client...
            self.__verify_method(name)

            # ...and local proxy method
            method = getattr(self, name)

            return method(args)

        except thriftpy.thrift.TApplicationException as tex:
            self.logger.error('Thrift error: %s' % tex)

        except Exception as ex:
            self.logger.error('Exception in dispatchCall(): %s' % ex)
            raise

    """
    Interface proxy method for RPC call createBucket

        @required args.name
        @return string token
    """
    def createBucket(self, args):

        thrift_client = self.thrift_client()
        thrift_module = self.thrift_module()

        # prepare CreateBucketRequest
        request = thrift_module.CreateBucketRequest()
        request.name = args.name

        # get CreateBucketResponse
        response = thrift_client.createBucket(request)

        # return the bucket token string
        return response.token

    """
    Interface proxy method for RPC call getTraces

        @required "token"
        @optional "type"
        @return list[] thrift.Trace
    """
    def getTraces(self, args):

        thrift_client = self.thrift_client()
        thrift_module = self.thrift_module()

        # prepare GetTracesRequest
        request = thrift_module.GetTracesRequest()

        try:
            request.token = args.token
            request.type = args.error_type
        except AttributeError as ex:
            self.logger.error('Missing required argument: %s' % ex)
            raise

        # get GetTracesResponse
        response = thrift_client.getTraces(request)

        # return list of traces
        return response.traces

class TracesHTTPController(TracesController):
    ''' Controller for (JSONized) HTTP requests to TracesHandler '''

    """
        @required content string <JSON data>
        @throws web.badrequest
        @throws web.ok
    """
    def POST(self):

        try:
            # check for Token: HTTP header as bucket id
            token = self.do_authentication()

            bucket = self.handler.get_bucket(token)

            data_json = web.data()
            data = json.loads(data_json)

            self.handler.create(bucket, data)

        except Exception as ex:
            self.logger.error('Caught exception in POST(): %s' % ex)
            raise web.badrequest()

        raise web.ok()

    """
        @required object data
        @return string JSON
    """
    def dump_json(self, data):
        return json.dumps(data)

    """
        @required HTTPHeader 'Token: <token>'
        @throws web.unauthorized
    """
    def do_authentication(self):

        token = web.ctx.env['HTTP_TOKEN']

        if not re.match(r'^[a-f0-9]{24}$', token):
            raise Exception("Invalid token")

        bucket = self.handler.get_bucket(token)

        if not bucket.get_token() == token:
            raise Exception("Token mismatch")

        return token
