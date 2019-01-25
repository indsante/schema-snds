import logging
import time


def initialize_logging() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def timeit(function_to_time):
    def timed(*args, **kwargs):
        start_time = time.time()
        result = function_to_time(*args, **kwargs)
        end_time = time.time()

        logger.info("{time:.2f} sec to execute function {function}".format(time=end_time - start_time,
                                                                           function=function_to_time.__name__))
        return result

    return timed
