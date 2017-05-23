# Get status of all datasets in all histories of a Galaxy instance
from bioblend import galaxy
from collections import defaultdict


def get_history_id(gi):

    histories = []
    history = gi.histories.get_histories()

    for item in history:
        for key, value in item.iteritems():
            if key == 'id':
                histories.append(value)
    return histories


def get_dataset_id(gi, histories):

    dataSetId = {}
    name = ''

    for hisId in histories:
        historyData = gi.histories.show_history(history_id=hisId)
        for key, value in historyData.iteritems():

            if key == 'name':
                name = value

            if key == 'state_ids':

                for status, data in value.iteritems():
                    if len(data) > 0:
                        dataSetId[name + ":" + hisId + ":" + status] = data
    return dataSetId


def get_dataset_metadata(gi, dataSetId):

    datasetMeta = defaultdict(dict)

    for status, litsId in dataSetId.iteritems():
        for dataId in litsId:
            metaData = gi.datasets.show_dataset(dataset_id=dataId)
            for key, value in metaData.iteritems():
                if key == "name":
                    datasetMeta[status][dataId] = value
    return datasetMeta


def main():

    apiFile = open("api-key.txt")
    url, key = apiFile.read().strip().split(',')

    gi = galaxy.GalaxyInstance(url=url, key=key)

    histories = get_history_id(gi)

    dataSetId = get_dataset_id(gi, histories)
    datasetMeta = get_dataset_metadata(gi, dataSetId)

    # print log
    for k, v in datasetMeta.iteritems():
        print k
        for item, name in v.iteritems():
            print " ", item, name


if __name__ == '__main__':
    main()