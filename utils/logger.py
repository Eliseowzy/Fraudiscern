#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ******************************************************************************
# Name: logger.py
# Developer: Wang Zhiyi (Based on Antoni Baum (Yard1) <antoni.baum@protonmail.com>)
# Data:
# Version:
# ******************************************************************************

import logging
import traceback


def get_logger() -> logging.Logger:
    try:
        assert bool(GLOBAL_LOGGER)
        return GLOBAL_LOGGER
    except:
        return create_logger()


def create_logger() -> logging.Logger:
    logger = logging.getLogger("logs")
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    if logger.hasHandlers():
        logger.handlers.clear()

    try:
        ch = logging.FileHandler("logs.log")
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


GLOBAL_LOGGER = create_logger()
