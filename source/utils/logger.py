# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi (Based on Antoni Baum (Yard1) <antoni.baum@protonmail.com>)
@file: logger.py
@time: 6/20/2021
@version: 1.0
"""

import logging
import traceback


def get_logger() -> logging.Logger:
    """Get a logger object, if not exists call _create_logger().

    Returns:
        class 'logging.Logger': A python logger object.
    """
    try:
        assert bool(GLOBAL_LOGGER)
        return GLOBAL_LOGGER
    except:
        return _create_logger()


def _create_logger() -> logging.Logger:
    """Create a logger object (singleton)

    Returns:
        class 'logging.Logger': A python logger object.
    """
    logger = logging.getLogger("logs")
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    if logger.hasHandlers():
        logger.handlers.clear()

    try:
        ch = logging.FileHandler("../../../logs/test.log")
    except:
        print("Could not attach a FileHandler to the logger! No logs will be saved.")
        traceback.print_exc()
        ch = logging.NullHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger


GLOBAL_LOGGER = _create_logger()
