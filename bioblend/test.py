# First test with bioblend on GenAP

from bioblend import galaxy
import sys
from collections import namedtuple
import pprint

f = open("api-key.txt")

key = f.read().strip()

#gi = galaxy.GalaxyInstance(url='http://masterv5-resub3.vzhost34.genap.ca:8088/galaxy', key='4b96673f3849e2cb55979552ee29664b')
gi = galaxy.GalaxyInstance(url='https://usegalaxy.org/', key='360ad40372de904e9f485f50a74221e9')


hist = gi.histories.get_histories()

# for item in hist:
#     for key, value in item.iteritems():
#         print key, value



# data =  gi.datasets.show_stdout()
#
# print data


# data = gi.datasets.show_dataset(dataset_id='bbd44e69cb8906b5861cd82ec71c6297', hda_ldda='hda')
# for i,j in data.iteritems():
#     print i, j

#
# a = gi.histories.show_history(history_id='56d87503b9d44022')
# for k,v in a.iteritems():
#     print k,v


##### RUN WORKFLOWW###########################################################
# my_workflows = gi.workflows._get()
#
# for work in my_workflows:
#     workflow = namedtuple("workflow", work.keys())(*work.values())
#
# print workflow
#
# input = gi.workflows.get_workflow_inputs(workflow_id='c48e74a956218c05', label='fastq')
#
# print input

wf = gi.workflows.show_workflow(workflow_id='c48e74a956218c05')
# pprint.pprint(wf)
print wf['inputs']

#
# meta = gi.workflows.invoke_workflow(workflow_id='c48e74a956218c05', inputs={ '0': {'id': 'bbd44e69cb8906b5da5d44ce8df707a0', 'src': 'hda'}},
#                                     history_name='Danouse')
#
# print meta

##########################################


# ############### Upload File #################
# file = gi.tools.upload_file(path="/Users/dmorais/Downloads/Galaxy_dataset_test/DAVID_TEST-GALAXY.bed", history_id='9fd8fbaec8d459d4',
#                             file_name="David_test.bed", dbkey='hg19')
# print file