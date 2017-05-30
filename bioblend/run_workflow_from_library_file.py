

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



############# GET Library folder and datasets ###################
    # lib_obj = gi.libraries.get_libraries(name='Demonstration Datasets')
    #
    # libre_obj = gi.libraries.show_library(library_id='6f124c2ade81ff6d', contents=True)
    #
    #
    # library = []
    # l = namedtuple('library', 'name id')
    #
    #
    # for item in libre_obj:
    #    if item['type'] == 'file':
    #        lib = l(item['name'], item['id'])
    #        library.append(lib)
    #
    # print library





############################ Create Library and folders ###################


    #lib_obj = gi.libraries.create_library(name="Test_API", description=" Testing Galaxy API")

    #folder_obj = gi.libraries.create_folder(library_id='613e73b56070623c', folder_name='sample_fastq')


################# Upload file from local path ################

    # loc_file_obj = gi.libraries.upload_file_from_local_path(library_id='613e73b56070623c',file_local_path='/Users/dmorais/scratch/python_scripts/AI/bioblend/datasets/Test.fastq',folder_id='Fd83646f216937eff')
    #
    # print loc_file_obj


############### Upload file from url to lib #########################

    url_file_obj = gi.libraries.upload_file_from_url(library_id='613e73b56070623c', file_url='https://datahub-qfw3js0t.udes.genap.ca/genap2/data-test/bcftools-test/concat.1.a.vcf',
                                                     file_type='vcf')

    print url_file_obj












if __name__ == "__main__":
    main()