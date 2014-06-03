'''
Module that provides the tools for logbuilder
'''

from . external import *

__all__ = ['log_with', 'setup_custom_logger']

# This class has a lowercase name because it is used as a decorator.
class log_with(object):
    '''
    Logging decorator that allows you to log function calls with a specific logger.

    Formats an log string based on the arguments and keywords passed to the function.

    Arguments
    ==========

    logger : logger supplied to decorator

    Keywords
    ========
    
    silent : bool
             Flag to specify if the logger is to remain silent.

    loglevel : str
               One of the strings defined in LOGLEVELS.
    '''

    LOGLEVELS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

    
    def __init__(self, logger, silent=False, loglevel='DEBUG'):
        self.mylog = logger
        self.silent = silent
        self.loglevel = loglevel

    def write_log(self, func, args, kwds):

        if len(args) > 0:
            arg_str = 'arguments: '
            for index, arg in enumerate(args):
                a_str = '{}'.format(arg)
                if len(a_str) > 40:
                    a_str = '{} of len(str({}))'.format(type(arg), len(a_str))
                if index == 0:
                    arg_str += ' {}'.format(a_str)
                else:
                    arg_str += ', {}'.format(a_str)
        else:
            arg_str = 'no arguments'

        if len(kwds) > 0:
            kwd_str = 'kwds: '
            for index, (key, value) in enumerate(kwds.items()):
                k_str = '{}={}'.format(key, value)
                if len(k_str) > 40:
                    k_str = '{}={} of len(str({}))'.format(key, type(value), len(k_str))
                if index == 0:
                    kwd_str += ' {}'.format(k_str)
                else:
                    kwd_str += ', {}'.format(k_str)
        else:
            kwd_str = 'no keywords'

        msg = 'Calling: {} with {} and {}'.format(func.__name__, arg_str, kwd_str)

        if self.loglevel == 'CRITICAL':
            self.mylog.critical(msg)
        elif self.loglevel == 'ERROR':
            self.mylog.error(msg)
        elif self.loglevel == 'INFO':
            self.mylog.info(msg)
        elif self.loglevel == 'DEBUG':
            self.mylog.debug(msg)
        elif self.loglevel not in self.LOGLEVELS:
            raise NotImplementedError('This log level has not yet been implemented: {}'.format(self.loglevel))
        
    def __call__(self, func):
        '''
        Returns a wrapper that wraps func.
        The wrapper will log the arguments and keyword arguments
        given to func at logging level DEBUG.
        '''

        @functools.wraps(func)
        def wrapper(*args, **kwds):
            if not self.silent:
                self.write_log(func, args, kwds)
            f_result = func(*args, **kwds)
            return f_result
        return wrapper
        
def setup_custom_logger(name, level=logging.DEBUG, logging_directory='log'):
    '''
    Creates a logger that outputs to its own file (logging_directory/name.log).
    
    Parameters
    ==========
    
    name  : str
            Name used to store this log under (typically the module name stored under __name__)
    
    level : int
            Default level to initiate log with (Default is set using logging.DEBUG)
            Can be changed with the custom_logger.setLevel function.
    
    logging_directory : str
            Directory to store log file in (defaults to logs) 
    
    Returns
    =======
    
    custom_logger
    '''
    
    if not os.path.exists(logging_directory):
        os.mkdir(logging_directory)
   
    class LevelFilter(logging.Filter):
        def __init__(self, level):
            self.level = level

        def filter(self, record):
            return record.levelno == self.level

    log_file = os.path.join(logging_directory, '{}.log'.format(name))
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s'))

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.addFilter(LevelFilter(logging.INFO))
    
    logger = logging.getLogger(name)

    logger.addHandler(fh)
    logger.addHandler(sh)

    logger.setLevel(level)
    
    logger.debug('Finished creating log file {} with logging level {}'.format(log_file, level)) 
    
    return logger    

mylog = setup_custom_logger(__name__)
mylog.debug('Finished defining logging tools {}'.format(__name__))
