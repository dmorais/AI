from collections import namedtuple
from bioblend import galaxy
import yaml

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



def get_galaxy_instance(api_key):
    '''
    :param api_key:
    :return: a galaxy instance object
    '''
    with open(api_key, 'r') as api:
        try:
            url, key = api.read().strip().split(',')
            gi = galaxy.GalaxyInstance(url=url, key=key)
            return gi

        except IOError:
            logger.error('Failed to open file api_key', exc_info=True)
            print "cannot open", api_key


def read_workflow(yaml_file):
    '''
    :param yaml_file:
    :return: workflow_exp: a list of named tuples (can be accessed as objects)
    '''

    workflows = ''
    workflow_exp = []
    with open(yaml_file, 'r') as stream:
        try:
            workflows = yaml.load(stream)

        except yaml.YAMLError as exc:
            logger.error('Failed to open file yaml file', exc_info=True)
            print exc

    # Create namedtuple from dictionary
    for work in workflows:
        workflow_nametup = namedtuple("workflow", work.keys())(*work.values())
        workflow_exp.append(workflow_nametup)

    return workflow_exp