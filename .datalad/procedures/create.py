#!/usr/bin/env python3
import os
import requests
import shutil
import sys
import zipfile

import datalad.api
from datalad.distribution.dataset import require_dataset

from git import Repo

ds = require_dataset(
    sys.argv[1],
    check_installed = True,
    purpose = 'setup empty dataset'
)

# remove files to be replaced
os.remove(".gitattributes")

# download empty-dataset template
res = requests.get("https://github.com/LAAC-LSCP/empty-dataset/archive/master.zip")
open("master.zip", "wb").write(res.content)

with zipfile.ZipFile("master.zip") as zip_file:
    for member in zip_file.namelist():
        filename = member.replace("empty-dataset-master/", "")

        source = zip_file.open(member)
        dest = os.path.join(sys.argv[1], filename)

        if os.path.isdir(filename) or filename.endswith('/'):
            os.makedirs(filename, exist_ok = True)
            continue

        if os.path.exists(dest):
            continue

        target = open(dest, "wb")

        with source, target:
            shutil.copyfileobj(source, target)

os.remove("master.zip")

open('.datalad/path', 'w+').write(os.path.join('/scratch1/data/laac_data/', os.path.basename(ds.path))

# commit everything
repo = Repo(sys.argv[1])
repo.git.add('*')
repo.git.commit(m = "initial commit")

# create github sibling
datalad.api.create_sibling_github(
    name = 'origin',
    reponame = os.path.basename(ds.path),
    dataset = ds,
    github_organization = 'LAAC-LSCP',
    access_protocol = 'ssh'
)

# create oberon sibling
datalad.api.create_sibling(
    name = 'cluster',
    dataset = ds,
    target_url = open('.datalad/path', 'r').read(),
    publish_depends = 'origin'
)