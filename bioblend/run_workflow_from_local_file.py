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
#
# UNFORTUNATELY a locally uploaded workflow will fail because
# Galaxy resets the input label (or name depending on the version) back to input dataset
# In this case open the workflow editor in Galaxy and rename the label (or name) of the inputs
# So it matches the label in the yaml file.
##############################################

import sys
from collections import namedtuple
import yaml
from bioblend import galaxy
import pprint
import os
import logging
from utils.giobjects import *
from utils.loggerinitializer import *
from distutils.dir_util import mkpath


mkpath(os.getcwd() + "/logs/")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
initialize_logger(os.getcwd() + "/logs/", logger)

def create_history(gi, name):
    '''
    :param gi: a  galaxy instance object
    :param name: history name
    :return: namedtuple with a (hist_name,hist_id)
    '''
    logger.info("Creating history")
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
    logger.info("Uploading file to Galaxy")
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
    logger.info("Getting workflow Id")
    workflows = []
    work_obj = gi.workflows.get_workflows()

    w = namedtuple('workflow', 'name id')
    work = ''

    if len(work_obj) == 0:
        name, w_id = _upload_workflow(gi, workflow_name, workflow_path)
        work = w(name, w_id)
        workflows.append(work)

    else:
        for item in work_obj:

            # If workflow already exist (or has been already auploaded via API) return its name and id
            if item['name'] == workflow_name or item['name'] + ' (imported from API)':
                work = w(item['name'], item['id'])
                workflows.append(work)

            # call upload method in and return the workflow name and id
            else:
                name, w_id = _upload_workflow(gi, workflow_name, workflow_path)
                work = w(name, w_id)
                workflows.append(work)


    return work


def _upload_workflow(gi, workflow_name, workflow_path):

    logger.info("Uploading new Workflow")
    work_obj = gi.workflows.import_workflow_from_local_path(file_local_path=workflow_path + workflow_name + ".ga")
    return work_obj['name'], work_obj['id']


def workflow_inputs(gi, workflow_id):
    '''
    :param gi:
    :param workflow_id:
    :return: a list of namedtuples of inputs (index, label)
    '''
    logger.info("Getting workflow inputs")
    workflow_input = []
    w = namedtuple('inputs', 'index label')

    work_obj = gi.workflows.show_workflow(workflow_id=workflow_id)

    for k, v in work_obj['inputs'].iteritems():
        w_input = w(k, v['label'])
        workflow_input.append(w_input)

    return workflow_input


def create_wf_input_dict(gi, datasets, inputs, data, labels):
    '''
    :param gi: galaxy instance object
    :param datasets: a list of namedtuples with dataset name, id
    :param inputs: a list of namedtuples with workflow inputs index, label
    :param data: a list with the inputs from the yaml file
    :param labels: a list with labels for each input (must be in the same order as the data list)
    :return: a dictionary of dictionary to be used as input in the workflow invocation
    '''

    logger.info("Creating input dictionary")
    input_dict = dict()
    label_dict = dict(zip(data, labels))

    # Map each dataset name to a label
    for item in datasets:
        if item.name in label_dict:
            label_dict[label_dict[item.name]] = item.id
            label_dict.pop(item.name)

    # Map each index to a label dictionary
    for item in inputs:
        if item.label in label_dict:
            input_dict[item.index] = {
                "id": label_dict[item.label],
                "src": "hda"
            }

    return input_dict


def run_workflow(gi, input, history_id, workflow_id):
    '''
    :param gi:
    :param input: a dictionary of dictionary with the inputs of each workflow
    :param history_id:
    :param workflow_id:
    :return: a dictionary with the pipeline invocation.
    '''

    logger.info("Invoking workflow")
    run_work_obj = gi.workflows.invoke_workflow(workflow_id=workflow_id, inputs=input, history_id=history_id)

    return run_work_obj


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

    # Loop through workflows in the yaml file
    for pipeline in yaml_file:
        history = create_history(gi, pipeline.name)
        datasets = upload_file(gi, pipeline.inputs, pipeline.inputs_path, history.id, pipeline.dbkey)
        g_workflow = get_workflow_id(gi, pipeline.name, pipeline.workflow_path)
        g_inputs = workflow_inputs(gi, g_workflow.id)
        input_dict = create_wf_input_dict(gi, datasets, g_inputs, pipeline.inputs, pipeline.inputs_label)
        invok_workflow = run_workflow(gi, input_dict, history.id, g_workflow.id)

    logger.info("DONE, check history when workflow completes")

if __name__ == "__main__":
    main()
