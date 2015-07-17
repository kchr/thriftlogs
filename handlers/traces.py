#!/usr/bin/env python
# coding: utf-8

import mongoengine

from model import Bucket, Trace


class TracesHandler:
    ''' Handler for Trace objects, used by TracesController instances '''

    def __init__(self):
        pass

    """ Get bucket by token """
    def get_bucket(self, token_id):
        try:
            buck = Bucket.objects.get(id=token_id)
            return buck
        except Exception:
            raise Exception("Bucket not found")

    """ Create bucket """
    def create_bucket(self, name):

        try:
            buck = Bucket.objects.get(name=name)
        except mongoengine.DoesNotExist:
            try:
                buck = Bucket()
                buck.name = name
                buck.save()
            except Exception:
                raise Exception("Failed to create bucket")

        return buck

    """ Get all objects """
    def get_list(self, token, error_type=None):

        traces = []

        # filter by token (bucket)
        where = {'token': token}

        # optional: filter by type
        if error_type is not None:
            where.update({'type': str(error_type)})

        try:
            for trace in Trace.objects(**where):
                traces.append(trace)

        except Exception:
            raise Exception("Failed to get list of objects")

        return traces

    """ Create new object """
    def create(self, bucket, data):

        if not isinstance(bucket, Bucket):
            raise Exception("Not a bucket")

        # try to create a new object
        try:
            trace = Trace()

            trace.token = bucket.get_token()
            trace.type = data.get('type')
            trace.message = data.get('message')
            trace.stack = data.get('stack', [])
            trace.context = data.get('context')

            trace.save()
            trace.reload()

            return self.format_trace(trace)

        except Exception:
            raise Exception("Failed to create object")

    """ Return a dict suitable for output """
    def format_trace(self, trace):

        return dict({
            "id": trace.get_id(),
            "type": trace.type,
            "message": trace.message,
            "stack": trace.stack,
            "context": trace.context
        })
