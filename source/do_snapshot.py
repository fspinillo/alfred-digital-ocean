import sys
from datetime import datetime
from workflow import Workflow, web, PasswordNotFound
import requests

def main(wf):
    #grab digital ocean token
    try:
        api_key = wf.get_password('digitalocean_api_key')
    except PasswordNotFound:
        wf.add_item('No API key set.',
                    'Please use dotoken to set your API key.',
                    valid = False)

    # get droplet id from previous script
    if len(wf.args):
        query = wf.args[0]

    # gather droplet information
    dropletData = requests.get('https://api.digitalocean.com/v2/droplets/' + query + '/', headers = {'Authorization': 'Bearer ' + api_key + ''}).json()

    # set the current date in YYYY-MM-DD format
    now = datetime.now()
    date = "%s-%s-%s" % (now.year, now.strftime("%m"), now.strftime("%d"))

    # set snapshot name based on droplet name and the date: dropletNAME-YYYY-MM-DD
    snapshotName = "%s-%s" % (dropletData['droplet']['name'], date)

    # build the URL and header information for creating a snapshot
    snapshotUrl = 'https://api.digitalocean.com/v2/droplets/' + query + '/actions'
    snapshotHeader = {'Authorization': 'Bearer ' + api_key + '', 'Content-Type': 'application/json'}
    snapshotPayload = {'type': 'snapshot', 'name': snapshotName}

    requests.post(snapshotUrl, params = snapshotPayload, headers = snapshotHeader)

if __name__=='__main__':
    wf = Workflow()
    sys.exit(wf.run(main))