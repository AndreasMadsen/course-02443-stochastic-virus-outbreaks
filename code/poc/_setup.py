"""sets path up for relative import"""

import sys
import os.path as path

THIS_DIR = path.dirname(path.realpath(__file__))
sys.path.append(path.join(THIS_DIR, "../"))
