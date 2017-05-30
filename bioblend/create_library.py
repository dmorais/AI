# This script create a Galaxy Library with subfolders
# and uploads datasets to it


import sys
from collections import namedtuple
import yaml
from bioblend import galaxy
import os
import logging
import pprint
from utils.giobjects import *
from utils.loggerinitializer import *
from distutils.dir_util import mkpath


mkpath(os.getcwd() + "/logs/")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
initialize_logger(os.getcwd() + "/logs/", logger)



def create_libary(gi, name, description):

    logger.info("Creating Library", name)
    lib_obj = gi.libraries.create_library(name=name, description=description)

    l = namedtuple('library', 'id name')
    library = l(lib_obj['id'], lib_obj['name'])

    return library


# def create_folder(gi, lib_id, name):
#
#
#     logger.info("Creating Folder ", name)
#     folder_obj = gi.libraries.create_folder(library_id=lib_id, folder_name=name)
#
#     f = namedtuple('folder', 'id name')
#     folder = f(folder_obj[0]['id'], folder_obj[0]['name'])
#
#     return folder



def main():
    if len(sys.argv) != 3:
        print "USAGE:\n\tpython {} api_key.txt yaml_file".format(sys.argv[0])
        logging.error("Bad args", exc_info=True)
        sys.exit(1)

    logger.info("############")
    api_key = sys.argv[1]
    yaml_file_name = sys.argv[2]

    gi = get_galaxy_instance(api_key)
    yaml_file = read_workflow(yaml_file_name)


    for item in yaml_file:

        library = create_libary(gi, item.name, item.description)
        #folder = create_folder(gi, library.id, item.folder)


    logger.info("Done")



if __name__ =="__main__":
    main()

