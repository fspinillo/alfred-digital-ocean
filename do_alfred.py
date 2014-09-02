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
                    'Please use dokey to set your API key.',
                    valid=False,
                    icon=ICON_WARNING)


    # builds the URL to access Digital Ocean API
    url = 'https://api.digitalocean.com/v2/droplets'
    header = {'Authorization': 'Bearer ' + api_key + ''}

    # gather the data, store the JSON and builds the array
    r = web.get(url, headers=header)
    data = r.json()
    droplet_array = data['droplets']

    # grabs the status of the droplets
    # checks for memory size, return is based on the memory size
    for droplet in droplet_array:
        if droplet['memory'] == 512:
            wf.add_item(title ='%s is %s on %s' % (
                droplet['name'],
                droplet['status'],
                droplet['region']['name']),
            subtitle = 'CPU(s): %s || Memory: %sMB || Size: %sGB' % (
                droplet['vcpus'],
                droplet['memory'],
                droplet['disk']))
        else:
            memory_string = str(droplet['memory'])
            wf.add_item(title ='%s is %s on %s' % (
                droplet['name'],
                droplet['status'],
                droplet['region']['name']),
            subtitle = 'CPU(s): %s || Memory: %sGB || Size: %sGB' % (
                droplet['vcpus'],
                memory_string[0],
                droplet['disk']))

    wf.send_feedback()

if __name__=='__main__':
    wf = Workflow()
    sys.exit(wf.run(main))