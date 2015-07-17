Logtrace 0.1
============

Prerequisities
--------------

You need a mongodb instance running somewhere within reach.

Requirements
------------

  - web.py
  - thriftpy
  - mongoengine

Installation
------------

Unpack the archive somewhere on your computer.

To install the required Python packages:

    $ make depends

Configuration
-------------

This project relies heavily on environment variables for its configuration:

    Variable name           Default    Description
    -----------------------------------------------------------------------

    MONGODB_HOST          127.0.0.1    MongoDB hostname
    MONGODB_PORT              27017    MongoDB port

    THRIFT_HOST           127.0.0.1    Thrift server bind hostname
    THRIFT_PORT                6000    Thrift server bind port
    THRIFT_FILE    tracelogs.thrift    Path to .thrift protocol file

Starting the servers
--------------------

**Thrift server**

    $ make thriftserve

**HTTP/JSON server**

    $ make webserve

Client usage
------------

To create buckets and list trace messages you need to use the thrift client:

    $ python ./client.py --help

Example for creating a new bucket:

    $ python ./client.py createBucket MyErrors
    55a9108145816363ee84a40d

The token you get in return is used to submit and retrieve errors from server.

List error messages in bucket:

    $ python ./client.py getTraces 55a9108145816363ee84a40d
    [Trace(message=u'This is an error aswell', type=u'IOError', stack=[], context=u'')]

HTTP/JSON API Usage
-------------------

Submit error messages to your bucket using HTTP/JSON:

    $ curl -i -X POST \
        -H 'Token: 55a9108145816363ee84a40d' \
        --data '{"message": "This is an error aswell", "type": "IOError"}' \
        http://localhost:8080/traces

