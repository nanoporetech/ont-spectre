import logging as logger

import numpy as np


class CoverageStatistics(object):
    # should have "get" and "set" func but just use them directly
    def __init__(self, as_dev=False):
        # {"average": np.nan, "std_dev": np.nan, "min": np.nan, "max": np.nan}
        # Stats
        logger.basicConfig(level=logger.DEBUG) if as_dev else logger.basicConfig(level=logger.INFO)
        self.logger = logger
        self.chromosome_len = 0
        self.chromosome_name = ""
        self.average = np.nan
        self.std_dev = np.nan
        self.min = np.nan
        self.max = np.nan
        self.median = np.nan

    def print(self):
        print_me = f'Statistics of chromosome {self.chromosome_name}' \
                   f'  chromosome length: {self.chromosome_len}\n' \
                   f'  average coverage: {self.average}\n' \
                   f'  median coverage: {self.median}\n' \
                   f'  standard deviation: {np.round(self.std_dev, 3)}\n' \
                   f'  min, max coverage: {np.round(self.min, 3)}, {np.round(self.max, 3)}\n'
        logger.info(print_me)


class CoverageData(object):
    # should have "get" and "set" func but just use them directly
    def __init__(self):
        # raw data
        self.coverage_raw = np.nan
        self.positions = np.nan
        self.coverage_log2 = np.nan         # log2(x)
        self.normalized_cov = np.nan        # x/median
        self.normalized_cov_ploidy = np.nan   # x/median * 2 -> for diploid
