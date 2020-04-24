#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2020 Mikołaj Machowski <mikmach@wp.pl>
# SPDX-License-Identifier: MIT
"""Separate files into zip packages with limited size.
   Store as complete files, not as split archive.
"""

import os
from zipfile import ZipFile

# Default limit for MNW Share - 1000MB
# make it safe with 950MB + possible zip overhead
LIMIT_SIZE = 950000000


def add_files_to_zip(archive_name: str, files: list):  # {{{
    """Add files to zip archive.
    archive_name - str - name of archive file
    files - list - list of files to compress

    Using default ZIP_STORED method (and looks like in Cygwin distribution no
    other compression methods are supported by zipfile module).
    We are sending already compressed files so we don't need real compression.
    It is more like unix tar command but for win communications.
    Write files in parent dir to avoid cluttering of current one.
    """
    with ZipFile('../'+archive_name, mode='w') as zf:
        for item in files:
            zf.write(item)

    # }}}


def file_size(fname: str) -> int:  # {{{
    """Check file size
    fname - str - file name
    return - int - file size in bytes
    """
    return os.stat(fname).st_size
    # }}}


def item_fail(fname: str, size: int) -> bool:  # {{{
    """Check if file is bigger than LIMIT_SIZE and raise SystemExit if yes.
    fname - str - file name
    size - int - file size in bytes
    return - bool
    """
    if size > LIMIT_SIZE:
        raise SystemExit(f'{fname} bigger than LIMIT_SIZE. Cannot proceed.')

    return True
    # }}}


def main():  # {{{
    """Main processing. """

    old_size = 0
    new_size = 0

    old_flist: list = []
    new_flist: list = []

    # Archive name, configurable from command line?
    # q'n'd way to get current dir as stem: last part of current dir path
    # at least it is system independent...
    arc_name_stem = os.path.split(os.getcwd())[-1]
    arc_name_item = 1
    arc_name = f'{arc_name_stem}{str(arc_name_item).zfill(3)}.zip'

    for file_name in os.listdir():

        item_size = file_size(file_name)
        item_fail(file_name, item_size)

        new_flist.append(file_name)
        new_size += item_size

        if new_size > LIMIT_SIZE:
            add_files_to_zip(arc_name, old_flist)
            arc_name_item += 1
            arc_name = f'{arc_name_stem}{str(arc_name_item).zfill(3)}.zip'
            new_flist = []
            new_size = 0
        else:
            old_size = new_size
            old_flist = new_flist

    add_files_to_zip(arc_name, old_flist)

    # }}}


if __name__ == '__main__':
    main()

# vim: ft=python tw=80 ts=8 et sw=4 sts=4 fdm=marker
