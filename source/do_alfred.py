import sys
import argparse
from workflow import Workflow, ICON_WEB, ICON_WARNING, web, PasswordNotFound
import requests

def main(wf):

    # parser to gather args from the acript
    parser = argparse.ArgumentParser()

    # saves the key to 'apikey'
    parser.add_argument('--setkey', dest='apikey', nargs='?', default=None)
    args = parser.parse_args(wf.args)

    # saving the api key
    if args.apikey:
        wf.save_password('digitalocean_api_key', args.apikey)
        return 0

    # verify that an API key has been set
    try:
        api_key = wf.get_password('digitalocean_api_key')
    except PasswordNotFound:
        wf.add_item('No API key set.',
                    'Please use dotoken to set your API key.',
                    valid=False,
                    icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    # build URL and header info for API request
    url = 'https://api.digitalocean.com/v2/droplets'
    header = {'Authorization': 'Bearer ' + api_key + ''}

    # gather the data, store the JSON and builds the array
    data = web.get(url, headers=header).json()

    droplet_array = data['droplets']

    # This is a multi-step process for checking on the status
    # It first checks the individual status of each droplet
    # If a droplet is current "in-progress" it will return what it's currently doing
    # If the droplet is not in an "in-progress" state, it returns general information

    for droplet in droplet_array:

        # get the current status of the individual droplets
        dropletID = droplet['id']
        statusURL = 'https://api.digitalocean.com/v2/droplets/%s/actions' % dropletID
        statusData = requests.get(statusURL, headers=header).json()

        # Returns what the droplet is doing if "in-progress"
        # Else it checks for memory size first, then returns basic information
        if statusData['actions'][0]['status'] == "in-progress":
            wf.add_item("%s is in the middle of a %s" % (droplet['name'], statusData['actions'][0]['type']))
        elif droplet['memory'] == 512:
            wf.add_item(title ='%s is %s on %s' % (
                droplet['name'],
                droplet['status'],
                droplet['region']['name']),
            subtitle = 'CPU(s): %s || Memory: %sMB || Size: %sGB' % (
                droplet['vcpus'],
                droplet['memory'],
                droplet['disk']),
            arg = str(droplet['id']),
            valid = True)
        else:
            memory_string = str(droplet['memory'])
            wf.add_item(title ='%s is %s on %s' % (
                droplet['name'],
                droplet['status'],
                droplet['region']['name']),
            subtitle = 'CPU(s): %s || Memory: %sGB || Size: %sGB' % (
                droplet['vcpus'],
                memory_string[0],
                droplet['disk']),
            arg = str(droplet['id']),
            valid = True)

    wf.send_feedback()

if __name__=='__main__':
    wf = Workflow()
    sys.exit(wf.run(main))