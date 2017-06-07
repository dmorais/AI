# Get status of all datasets in all histories of a Galaxy  instance
from bioblend import galaxy
from collections import namedtuple
from collections import defaultdict
import logging
from utils.giobjects import *
from utils.loggerinitializer import *
from distutils.dir_util import mkpath
import sys

mkpath(os.getcwd() + "/logs/")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
initialize_logger(os.getcwd() + "/logs/", logger)

# def get_history_id(gi):
#
#     histories = []
#     hist_obj = gi.histories.get_histories()
#     print history
#     sys.exit(0)
#
#     for item in history:
#         for key, value in item.iteritems():
#             if key == 'id':
#                 histories.append(value)
#
#     return histories


# def get_dataset_id(gi, hist_id):
#
#
#     dataset_obj = gi.histories.show_history(history_id=hist_id)
#     return dataset_obj['state_ids']

    # for k, v in sorted(dataset_obj['state_ids'].iteritems()):
    #     print k, "->", v


    # # print dataset_obj['state_ids']
    #
    # # for meta in dataset_obj.keys():
    # #
    # #     if meta == 'state_ids':
    # #         print meta[0]
    # #         # for k, v in meta.iteritems():
    # #         #     print k, "->", v
    #
    # sys.exit()
    #
    # # dataSetId = {}
    # # name = ''
    # #
    # # for hisId in histories:
    # #     historyData = gi.histories.show_history(history_id=hisId)
    # #     for key, value in historyData.iteritems():
    # #
    # #         if key == 'name':
    # #             name = value
    # #
    # #         if key == 'state_ids':
    # #
    # #             for status, data in value.iteritems():
    # #                 if len(data) > 0:
    # #                     dataSetId[name + ":" + hisId + ":" + status] = data
    # # return dataSetId


# def get_dataset_metadata(gi, dataSetId):
#
#     datasetMeta = defaultdict(dict)
#
#     for status, litsId in dataSetId.iteritems():
#         for dataId in litsId:
#             metaData = gi.datasets.show_dataset(dataset_id=dataId)
#             for key, value in metaData.iteritems():
#                 if key == "name":
#                     datasetMeta[status][dataId] = value
#     return datasetMeta

def get_datset_name(gi, d_id):


    data_name_obj = gi.datasets.show_dataset(dataset_id=d_id)

    return data_name_obj['name']


def main():

    gi = get_galaxy_instance("api-key.txt",logger)

    histories = get_history(gi)
    metadata = {}

    for history in histories:
        dataset_id = get_dataset_id(gi, history.id)
        metadata[history.name + "_" + history.id] = dataset_id


    for hist, states in metadata.iteritems():
        print "\n", hist
        for state, id in sorted(states.iteritems(), reverse=True):
            if (state == 'ok' or state=='discarded' or state=='error' or state=='running') and len(state) > 0:
                print state, "->",

                for data_id in id:
                    print data_id, get_datset_name(gi,data_id)

        print "\n"

    # print histories
    # sys.exit()
    #
    # dataSetId = get_dataset_id(gi, histories)
    # datasetMeta = get_dataset_metadata(gi, dataSetId)
    #
    # # print log
    # for k, v in datasetMeta.iteritems():
    #     print k
    #     for item, name in v.iteritems():
    #         print " ", item, name


if __name__ == '__main__':
    main()