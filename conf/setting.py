import logging
import os
import sys

import yaml

DIR_PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DIR_PATH)

LOG_LEVEL = logging.DEBUG
SYSTEM_LOG_LEVEL = logging.DEBUG

FILE_PATH = {
    'extract': os.path.join(DIR_PATH, 'testcase/extract.yaml'),
    'conf': os.path.join(DIR_PATH, 'conf/config.ini'),

}

print(FILE_PATH['extract'])
