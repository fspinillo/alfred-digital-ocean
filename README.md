Quickly grab the status of your Digital Ocean droplets by typing digitalocean


The workflow uses standard Python packages, expcet for Workflow, so no additional requirements needed. Workflow is bundled in the file, and was created by [Dean Jackson (deanishe)](https://github.com/deanishe/alfred-workflow/).
![alfred-preview](http://i.imgur.com/eXnpsmG.png)

Setup
---
1. To set this up you'll first need get a token from your [settings](https://cloud.digitalocean.com/settings/applications) page.

2. Run 'dotoken', and this will let you paste your token

3. A notification will display letting you know the token was saved

Using the workflow
---
Run 'dos' to pull up the status of your droplet(s)

Todo
---
1. Store the droplet names locally
2. Read from the stored data to trigger actions with your droplets: shutdown, power cycle, restart, etc

Warning
---
I currently am only running 1 droplet, so I have not be able to test this yet for multiple droplets.
