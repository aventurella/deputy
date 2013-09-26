"""You can leave casefiles for the deputy at her desk. She'll search
her desk (project-root/casefiles) for casefiles when looking for things to do.

"""

import os
import sys
import glob
import re
import importlib

CASEFILES_DIR_NAME = 'casefiles'
CASEFILES_DIR = os.getcwd() + '/' + CASEFILES_DIR_NAME


def search(casefile_name, casefiles_dir=CASEFILES_DIR):
    casefiles = collect(casefiles_dir)
    matched_result = None

    for raw_casefile in casefiles:
        if casefile_name in raw_casefile:
            matched_result = raw_casefile
            break

    if matched_result is not None:
        try:
            casefile = import_raw_casefile(matched_result)
        except ImportError:
            raise
        else:
            return casefile
    else:
        # TODO: Revisit - Raise cutom error here.
        raise NameError('Could not find matching name on the desktop!')


def collect(casefiles_dir=CASEFILES_DIR):
    casefiles = []

    # Filter out paths with dunder file names.
    filter_re = r'.*__.py$'

    try:
        casefiles = [ i for i in glob.glob(casefiles_dir + '/*.py') \
            if not re.search(filter_re, i)]

    except OSError:
        raise

    return casefiles


# Helpers
# ============================================================================

def import_raw_casefile(raw_casefile):
    path, file_name = raw_casefile.rsplit('/', 1)

    update_sys_path(path)

    try:
        casefile = importlib.import_module(file_name.strip('.py'))
    except ImportError:
        raise
    else:
        return casefile


def update_sys_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)
