#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
from sasila.slow_system.utils import logger
import traceback
import time


def checkResponse(func):
    @functools.wraps(func)
    def wrapper(self, response):
        if not response.m_response:
            if response.m_response is None:
                logger.error(
                        'response.m_response is None and url : ' + response.request.url + ' and request has been push to queue again!')
            else:
                logger.error(
                        'response.m_response is failed 【' + str(
                                response.m_response.status_code) + '】 and url : ' + response.request.url + ' content:' + response.m_response.content + ' and request has been push to queue again!')
            yield response.request
        else:
            process = func(self, response)
            if process is not None:
                try:
                    for callback in process:
                        yield callback
                except Exception:
                    logger.error(
                            'process error: ' + response.request.url + '\r\n' + response.m_response.content + '\r\n' + traceback.format_exc())

    return wrapper


def checkResponseWithTime(func):
    @functools.wraps(func)
    def wrapper(self, response):
        if not response.m_response:
            if response.m_response is None:
                logger.error(
                        'response.m_response is None and url : ' + response.request.url + ' and request has been push to queue again!')
            else:
                logger.error(
                        'response.m_response is failed 【' + str(
                                response.m_response.status_code) + '】 and url : ' + response.request.url + ' content:' + response.m_response.content + ' and request has been push to queue again!')
            yield response.request
        else:
            process = func(self, response)
            if process is not None:
                try:
                    start = time.clock()
                    for callback in process:
                        yield callback
                    logger.info(func.__name__ + ' run time: ' + '{:.9f}'.format(time.clock() - start))
                except Exception:
                    logger.error(
                            'process error: ' + response.request.url + '\r\n' + response.m_response.content + '\r\n' + traceback.format_exc())

    return wrapper


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.clock()
        ret = func(*args, **kwargs)
        logger.info(func.__name__ + ' run time: ' + '{:.9f}'.format(time.clock() - start))
        return ret

    return wrapper


def timeit_generator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        rets = func(*args, **kwargs)
        start = time.clock()
        for ret in rets:
            yield ret
        logger.info(func.__name__ + ' run time: ' + '{:.9f}'.format(time.clock() - start))

    return wrapper


def tryCatch(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ret
        except Exception:
            logger.info('【%s】error:%s' % (func.__name__, traceback.format_exc()))

    return wrapper


def tryCatch_generator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            rets = func(*args, **kwargs)
            for ret in rets:
                yield ret
        except Exception:
            logger.info('【%s】error:%s' % (func.__name__, traceback.format_exc()))

    return wrapper
