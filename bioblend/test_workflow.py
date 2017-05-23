############################################################
# This script test a workflow in a given Galaxy instance
#
#    1- It reads the api-key.txt file (a csv) with two fields
#         url (galaxy address),key ( Galaxy AI key)
#    2- It reads a yaml file with the workflow name and inputs
#    3- It creates a history
#    4- Upload the inputs
#    5- Upload the workflow
#    6- Get the workflow id and inputs
#    7- builds the input dictionary
#    8- runs the workflow
############################################

from bioblend import galaxy
from collections import defaultdict, namedtuple
import pprint
import yaml
import sys


def get_galaxy_instance(api_key):

    with open(api_key, 'r') as api:
        try:
            url, key = api.read().strip().split(',')
            gi = galaxy.GalaxyInstance(url=url, key=key)
            return gi

        except IOError:
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
            print exc

    # Create namedtuple from dictionary
    for work in workflows:
        workflow_nametup = namedtuple("workflow", work.keys())(*work.values())
        workflow_exp.append(workflow_nametup)

    return workflow_exp

    # THIS IS HOW TO LOOP THROUGH EACH WORKFLOW
    # for item in workflow_exp:
    #     print item.name


def create_history(gi, name):
    '''
    :param gi: a  galaxy instance object
    :param name: history name
    :return: namedtuple with a (hist_name,hist_id)
    '''

    data = namedtuple("history", 'name id')

    new_hist = gi.histories.create_history(name=name)
    history = data(new_hist['name'], new_hist['id'])

    return history


def upload_file(gi, input, hist_id, dbkey=None):
    '''

    :param gi: a galaxy instance object
    :param input: a list of input files
    :param hist_id: history ID
    :param dbkey: a list of dbkey (optional)
    :return: A list of namedtuples with dataset (name,id)
    '''

    dataset = []

    for i in range(len(input)):
        if len(dbkey) > i:
            file = gi.tools.upload_file(path=input[i], history_id=hist_id, dbkey=dbkey[i])
        else:
            file = gi.tools.upload_file(path=input[i], history_id=hist_id)

        d = namedtuple("dataset", 'name id')
        data = d(file['outputs'][0]['name'], file['outputs'][0]['id'])

        dataset.append(data)

    print dataset


def main():

    if len(sys.argv) != 3:
        print "USAGE:\n\tpython {} api_key.txt yaml_file".format(sys.argv[0])
        sys.exit(1)

    api_key = sys.argv[1]
    yaml_file = sys.argv[2]

    gi = get_galaxy_instance(api_key)
    workflow_exp = read_workflow(yaml_file)



    # #Loop through workflows in the yaml file

    for workflow in workflow_exp:

        history = create_history(gi, workflow.name)
        upload_file(gi, workflow.inputs, history.id, workflow.dbkey)


if __name__ == "__main__":
    main()
