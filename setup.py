import os
import sys
import requests
import time
import datetime as dt
import random
import json
import re

"""
created @ 2021-05-24
0.  try to download public information from Shanghai and Shenzhen security exchange websites.

"""

save_dir = os.path.join(".", "data")
