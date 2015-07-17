import logging

# if 'log' not in globals():
logger = logging.getLogger()

logging.basicConfig()

def logsetup(args={}):
    if args.get('verbose', False):
        logger.setLevel(logging.DEBUG)
    elif args.get('silent', False):
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.INFO)

#if __name__ == "__main__":
#    print "in __main__"
#    # print "log not found, running getlogger()"
