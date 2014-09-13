import sys
import argparse
from workflow import Workflow, ICON_WEB, ICON_WARNING, web, PasswordNotFound

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

    url = 'https://api.digitalocean.com/v2/droplets'
    header = {'Authorization': 'Bearer ' + api_key + ''}

    # gather the data, store the JSON and builds the array
    r = web.get(url, headers=header)
    data = r.json()
    droplet_array = data['droplets']

    for droplet in droplet_array:
        # Check to see if droplet is active. If it is active it lets the user # know they need to power off the droplet first.
        # After the check, the droplet status is returned
        # Selecting a droplet will pass its ID into Alfred for the next script

        if droplet['status'] == 'active':
            wf.add_item(title = '%s is still active' % droplet['name'],
                subtitle = 'Please power off before creating snapshot')
        else:
            if droplet['memory'] == 512:
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