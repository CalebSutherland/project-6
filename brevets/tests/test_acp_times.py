"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

from acp_times import open_time, close_time
import arrow
import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


def test_brevet1():
    start_time = arrow.get("2023-01-10 00:00", "YYYY-MM-DD HH:mm")
    dist = 200
    checkpoints = {
            0: (start_time, start_time.shift(hours=1)),
            20: (start_time.shift(minutes=35), start_time.shift(hours=2)),
            60: (start_time.shift(hours=1, minutes=46), start_time.shift(hours=4)),
            100: (start_time.shift(hours=2, minutes=56), start_time.shift(hours=6, minutes=40)),
            200: (start_time.shift(hours=5, minutes=53), start_time.shift(hours=13.5)),
            220: (start_time.shift(hours=5, minutes=53), start_time.shift(hours=13.5))
            }

    for km, times in checkpoints.items():
        check_open, check_close = times
        logging.debug("CHECK")
        logging.debug(check_close)
        logging.debug("TIME")
        logging.debug(close_time(km, dist, start_time))
        assert(open_time(km, dist, start_time)) == check_open
        assert(close_time(km, dist, start_time)) == check_close


def test_brevet2():
    start_time = arrow.get("2023-01-10 00:00", "YYYY-MM-DD HH:mm")
    dist = 300
    checkpoints = {
            50: (start_time.shift(hours=1, minutes=28), start_time.shift(hours=3, minutes=30)),
            150: (start_time.shift(hours=4, minutes=25), start_time.shift(hours=10)),
            200: (start_time.shift(hours=5, minutes=53), start_time.shift(hours=13, minutes=20)),
            250: (start_time.shift(hours=7, minutes = 27), start_time.shift(hours=16, minutes=40)),
            300: (start_time.shift(hours=9), start_time.shift(hours=20))
            }


    for km, times in checkpoints.items():
        check_open, check_close = times
        assert(open_time(km, dist, start_time)) == check_open
        assert(close_time(km, dist, start_time)) == check_close


def test_brevet3():
    start_time = arrow.get("2023-01-10 00:00", "YYYY-MM-DD HH:mm")
    dist = 400
    checkpoints = {
            40: (start_time.shift(hours=1, minutes=11), start_time.shift(hours=3)),
            200: (start_time.shift(hours=5, minutes=53), start_time.shift(hours=13, minutes=20)),
            300: (start_time.shift(hours=9), start_time.shift(hours=20)),
            400: (start_time.shift(hours=12, minutes = 8), start_time.shift(days=1, hours=3)),
            440: (start_time.shift(hours=12, minutes = 8), start_time.shift(days=1, hours=3)),
            }

    for km, times in checkpoints.items():
        check_open, check_close = times
        assert(open_time(km, dist, start_time)) == check_open
        assert(close_time(km, dist, start_time)) == check_close


def test_brevet4():
    start_time = arrow.get("2023-01-10 00:00", "YYYY-MM-DD HH:mm")
    dist = 600
    checkpoints = {
            150: (start_time.shift(hours=4, minutes=25), start_time.shift(hours=10)),
            200: (start_time.shift(hours=5, minutes=53), start_time.shift(hours=13, minutes=20)),
            300: (start_time.shift(hours=9), start_time.shift(hours=20)),
            400: (start_time.shift(hours=12, minutes = 8), start_time.shift(days=1, hours=2, minutes=40)),
            600: (start_time.shift(hours=18, minutes = 48), start_time.shift(days=1, hours=16))
            }


    for km, times in checkpoints.items():
        check_open, check_close = times
        assert(open_time(km, dist, start_time)) == check_open
        assert(close_time(km, dist, start_time)) == check_close


def test_brevet5():
    start_time = arrow.get("2023-01-10 00:00", "YYYY-MM-DD HH:mm")
    dist = 1000
    checkpoints = {
            50: (start_time.shift(hours=1, minutes=28), start_time.shift(hours=3.5)),
            150: (start_time.shift(hours=4, minutes=25), start_time.shift(hours=10)),
            300: (start_time.shift(hours=9), start_time.shift(hours=20)),
            500: (start_time.shift(hours=15, minutes = 28), start_time.shift(days=1, hours=9, minutes=20)),
            800: (start_time.shift(days=1, hours=1, minutes = 57), start_time.shift(days=2, hours=9.5)),
            1000: (start_time.shift(days=1, hours=9, minutes = 5), start_time.shift(days=3, hours=3)),
            1100: (start_time.shift(days=1, hours=9, minutes = 5), start_time.shift(days=3, hours=3))
            }


    for km, times in checkpoints.items():
        check_open, check_close = times
        logging.debug("CHECK")
        logging.debug(check_close)
        logging.debug("TIME")
        logging.debug(close_time(km, dist, start_time))
        assert(open_time(km, dist, start_time)) == check_open
        assert(close_time(km, dist, start_time)) == check_close

