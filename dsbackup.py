#!/usr/bin/env python

import calendar
import fnmatch
import os
import shutil
import subprocess
import time

DS_BACKUP = '.ds_backup'

DOWNLOAD_CMD = 'gsutil -m cp -r gs://%s %s'

def download_backup(bucket_name):
    if os.path.exists(DS_BACKUP):
        shutil.rmtree(DS_BACKUP)

    os.makedirs(DS_BACKUP)

    cmd = DOWNLOAD_CMD % (bucket_name, DS_BACKUP)
    subprocess.check_output(cmd.split(' '))


def get_files():
    matches = []
    for root, dirnames, filenames in os.walk(DS_BACKUP):
        for filename in fnmatch.filter(filenames, 'output-*'):
            matches.append(os.path.join(root, filename))
    return matches


if __name__ == '__main__':
    if len(sys.argv) == 1:
        download_backup(sys.argv[1])
    else:
        sys.exit(1)
