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

    hist_obj = gi.histories.create_history(name=name)
    history = data(hist_obj['name'], hist_obj['id'])

    return history


def upload_file(gi, input, input_path, hist_id, dbkey=None):
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
            file_obj = gi.tools.upload_file(path=input_path + input[i], history_id=hist_id, dbkey=dbkey[i])
        else:
            file_obj = gi.tools.upload_file(path=input_path + input[i], history_id=hist_id)

        d = namedtuple('dataset', 'name id')
        data = d(file_obj['outputs'][0]['name'], file_obj['outputs'][0]['id'])
        dataset.append(data)

    return dataset


def get_workflow_id(gi, workflow_name, workflow_path):
    '''

    :param gi: a galaxy instance object
    :param workflow_name: workflow name (str)
    :param workflow_path: workflow path (str)
    :return: a namedtuples with workflow name, id
    '''

    workflows = []
    work_obj = gi.workflows.get_workflows()

    w = namedtuple('workflow', 'name id')
    work = ''
    for item in work_obj:

        # If workflow already exist (or has been already auploaded via API) return its name and id
        if item['name'] == workflow_name or item['name'] + ' (imported from API)':
            work = w(item['name'], item['id'])
            workflows.append(work)

        # call upload method in and return the workflow name and id
        else:
            name, w_id = _upload_workflow(gi,workflow_name, workflow_path)
            work = w(name, w_id)
            workflows.append(work)

    return work


def _upload_workflow(gi, workflow_name, workflow_path):

    work_obj = gi.workflows.import_workflow_from_local_path(file_local_path=workflow_path + workflow_name + ".ga")

    return work_obj['name'], work_obj['id']


def workflow_inputs(gi, workflow_id):


    work_obj = gi.workflows.show_workflow(workflow_id=workflow_id)

    print work_obj['inputs']


# wf = gi.workflows.show_workflow(workflow_id='c48e74a956218c05')
# # pprint.pprint(wf)
# print wf['inputs']

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

        # history = create_history(gi, workflow.name)
        # datasets = upload_file(gi, workflow.inputs, workflow.inputs_path, history.id, workflow.dbkey)
        g_workflow = get_workflow_id(gi, workflow.name, workflow.workflow_path)
        inputs = workflow_inputs(gi, g_workflow.id)


if __name__ == "__main__":
    main()
