#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Clint Savage- @herlo <herlo1@gmail.com>
#
# Manage the spin up of duffy nodes.
# See https://wiki.centos.org/QaWiki/CI/Duffy for more information about
# duffy.
#

#---- Documentation Start ----------------------------------------------------#
DOCUMENTATION = '''
---
version_added: "0.1"
module: duffy
short_description: Duffy instance managemer
description:
  - This module allows a user to manage any number of duffy systems.
options:
  name:
    description:
      Given name for task
  state:
    description:
      Allocate or Deallocate instances
    required: true
  group:
    description:
      Group to which machine belongs. Useful when provisioning multiple machines
    default: name
  count:
    description:
      Number of instances to allocate
    default: 1
  key_path:
    description:
      Path to duffy.key
    default: ~/duffy.key
  version:
    description:
      Version of CentOS to provision
    choices: [5, 6, 7]
    default: 7
  arch:
    description:
    choices: [ 'x86_64', 'i386' ]
    default: 'x86_64'


notes:
  - See https://wiki.centos.org/QaWiki/CI/Duffy for more information
    required: true
requirements: []
author: Clint Savage - @herlo
'''

EXAMPLES = '''
- name: "provision nodes in group herlo-ci"
  duffy:
    state: present
    count: 4
    group: herlo-ci

# teardown any nodes in group 'herlo-ci'
- name: "teardown openshift nodes"
  duffy:
    state: absent
    group: herlo-ci

'''

#---- Logic Start ------------------------------------------------------------#
import json, urllib, subprocess, sys, os, time

from ansible.constants import mk_boolean
from ansible.module_utils.basic import *


class Duffy:

    def __init__(self):
        pass

    def allocate(self):
        b=json.load(urllib.urlopen(get_nodes_url))
        hosts=b['hosts']
        ssid=b['ssid']
        print("Allocated {} hosts with DUFFY_SSID={}".format(len(hosts), ssid))
#        return hosts, ssid

    def execute(self, module):

        state = module.params['state']

        # allocate some systems if state is 'present' :)
        if state == 'present':

            url_base="http://admin.ci.centos.org:8080"
            api_key=open(os.path.expanduser(module.params['key_path'])).read().strip()
            ver=module.params['version']
            arch=module.params['arch']
            count=module.params['arch']

            self.get_url="{0}/Node/get?key={1}&ver={2}&arch={3}&count={4}".format(url_base,api_key,ver,arch,count)

#            self.allocate()


        module.exit_json(changed=True)


def main():

    module = AnsibleModule(
        argument_spec=dict(
            name = dict(type='str'),
            state = dict(choices=['present', 'absent'], default='present'),
            group = dict(default=None, type='str'),
            count = dict(default=1, type='int'),
            version = dict(default=7, type='int'),
            arch = dict(default='x86_64', type='str'),
            key_path = dict(default='~/duffy.key', type='str'),
        ),
    )

    groupname = module.params.get('group')
    if groupname is None:
        module.params['group'] = module.params['name']

    try:
        d = Duffy()
        d.execute(module)
    except Exception as e:
        module.fail_json(msg=str(e))


#---- Import Ansible Utilities (Ansible Framework) ---------------------------#
main()
