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



def get_workflow_id(gi, workflow_name, logger, workflow_path=None):
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