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
