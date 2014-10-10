Digital Ocean's API is still in beta, so this will be evolving as their API access evolves.

This workflow allows you to interact with your droplets to perform various functions. Currently you can do the follow:

* Get the current status of your droplets
* Reboot a droplet
* Shutdown a droplet
* Power cycle a dropet
* Power on a droplet
* Create snapshots of a droplet

The workflow uses standard Python packages, expcet for Workflow, so no additional requirements needed. Workflow is bundled in the file, and was created by [Dean Jackson (deanishe)](https://github.com/deanishe/alfred-workflow/).

Setup
---
1. To set this up you'll first need get a token from your [settings](https://cloud.digitalocean.com/settings/applications) page.

2. In order to control droplets you need to set your token scope to **write**. If it is not set to write you wont be able to power on, shutdown, or take snapshots

3. Run 'dotoken', and this will let you paste your token

4. A notification will display letting you know the token was saved

Using the workflow
---
Status:  
'dos' will return information pertaining to your droplets. You will get back activity status, name, CPUs, RAM, and HDD size. If the droplet is in the middle of a task it will inform you.

Shutdown:  
After running 'dos', hold down ctrl to pick a droplet to shutdown.

Reboot:  
After running 'dos', hold down alt to pick a droplet to reboot.

Power-on:  
After running 'dos', hold down cmd to pick a droplet to power-on.

Power-cycle:  
After running 'dos', hold down fn to pick a droplet to power-cycle.

Snapshots:  
'sshot' will check to see which droplets are currently off. If a droplet is not off, it will inform you to power it down first. Select a powered down droplet and hit enter to initiate the snapshot. Snapshots are generated based on the name and date. Example: DropletName-YYYY-MM-DD

Todo
---
1. Store the droplet information locally for quicker access
2. Return more infomration in the notification
