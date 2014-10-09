import sys
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

    # pass droplet ID into workflow
    if len(wf.args):
        query = wf.args[0]

    # Build URL based on droplet ID, and generate header information from API key
    url = 'https://api.digitalocean.com/v2/droplets/' + query + '/actions'
    header = {'Authorization': 'Bearer ' + api_key + '', 'Content-Type': 'application/json'}
    payload = {'type': 'shutdown'}

    requests.post(url, params = payload, headers = header)

if __name__=='__main__':
    wf = Workflow()
    sys.exit(wf.run(main))