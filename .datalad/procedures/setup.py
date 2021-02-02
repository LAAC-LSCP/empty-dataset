#!/usr/bin/env python3

import sys
import os

import datalad.api
from datalad.distribution.dataset import require_dataset

ds = require_dataset(
    sys.argv[1],
    check_installed=True,
    purpose='configuration'
)

url = open(os.path.join(sys.argv[1], '.datalad/path')).read().strip()
if len(sys.argv) > 2:
    url = "{}:{}".format(sys.argv[2], url)

datalad.api.siblings(
    dataset = ds,
    action = 'configure',
    name = 'cluster',
    publish_depends = 'origin',
    url = url
)