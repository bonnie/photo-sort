"""organizing photos by date in my dropbox backup folder, from other places
where they may have landed"""

import os
import shutil
import datetime

OSX_PHOTOPATH = '/Users/bonnie/Pictures/Photos Library.photoslibrary/Masters'

# file to track folders that have already been processed
OSX_ALREADY_PROCESSED = 'osx_already_processed.txt'

PHOTOPATH = '/Users/bonnie/Dropbox/backup/Pictures'
DUPPATH = os.path.join(PHOTOPATH, 'duplicates')


def make_directory(dirname):
    """create a directory and tell the world about it"""

    if not os.path.exists(dirname):
        os.mkdir(dirname)
        print "*****made directory", dirname


def place_photo(item, parent_dir, copy=False):
    """given the full path to a photo, move or copy it to the backup dir"""

    item_fullpath = os.path.join(parent_dir, item)

    if os.path.isfile(item_fullpath) and item[0] != '.':
        file_date_unix = os.path.getmtime(item_fullpath)
        file_date = datetime.datetime.fromtimestamp(file_date_unix)
        year = file_date.strftime('%Y')

        # make year dir if it doesn't exist
        yeardir = os.path.join(PHOTOPATH, year)
        make_directory(yeardir)

        # final foldername is the actual date
        foldername = file_date.strftime('%Y-%m-%d')
        dirname = os.path.join(yeardir, foldername)

        if not os.path.exists(dirname):
            alternate_foldername = file_date.strftime('%Y_%m_%d')
            alternate_dirname = os.path.join(yeardir, alternate_foldername)

            # rename or create folder as needed
            if os.path.exists(alternate_dirname):
                os.rename(alternate_dirname, dirname)
                print "*****renamed directory", alternate_dirname, "to", dirname
            else:
                make_directory(dirname)

        # if the photo is already there, and duplicates have been requested,
        # copy it to the dup dir. Otherwise, bail.
        if os.path.exists(os.path.join(dirname, item)):
            dest = DUPPATH
        else:
            dest = dirname

        if copy:
            shutil.copy(item_fullpath, dest)
            action = "copied"
        else:
            shutil.move(item_fullpath, dest)
            action = "moved"

        print action, item_fullpath, "to", dest


def organize_loose():
    """organize loose photos in the PHOTOPATH directory"""

    for item in os.listdir(PHOTOPATH):
        place_photo(item, PHOTOPATH)


def organize_osx_photos():
    """copy photos from the OSX photos app to dropbox backup

    take care to spend as little time as possible on already-processed folders
    """

    # load in all the dirs we've already processed
    history_file = open(OSX_ALREADY_PROCESSED, 'r')
    last_date = history_file.read().rstrip()
    history_file.close()

    history_file = open(OSX_ALREADY_PROCESSED, 'w')

    # get the latest date we are looking at
    lyear, lmonth, lday = last_date.split('-')

    # drill down
    for year in os.listdir(OSX_PHOTOPATH):
        if year < lyear:
            continue
        yeardir = os.path.join(OSX_PHOTOPATH, year)

        for month in os.listdir(yeardir):
            if month < lmonth:
                continue
            monthdir = os.path.join(yeardir, month)

            for date in os.listdir(monthdir):
                if date < lday:
                    continue

                # if we got here, the directory needs to be processed
                datedir = os.path.join(monthdir, date)

                # for fun, osx puts each file in its own special directory
                for container in os.listdir(datedir):
                    container_dir = os.path.join(datedir, container)
                    for photo in os.listdir(container_dir):
                        place_photo(
                            item=photo,
                            parent_dir=container_dir,
                            copy=True)

    # write the last date to the file
    history_file.write('-'.join([year, month, date]))
    history_file.close()

# end organize_osx_photos #

##### Main ######

# create duplicate repository if it doesn't exist
make_directory(DUPPATH)

organize_loose()
organize_osx_photos()
