from collections import namedtuple
from bioblend import galaxy


def get_history(gi, name=None):
    '''
    :param gi: Galaxy instance object
    :param name: (optional) history name
    :return: a list of namedtuples (name, id)
    '''

    histories = []
    history_obj = gi.histories.get_histories()
    h = namedtuple('history', 'name id')

    for item in history_obj:

        if item['name'] == name:
            hist = h(item['name'], item['id'])
            histories.append(hist)
            break
        else:
            hist = h(item['name'], item['id'])
            histories.append(hist)

    return histories