#!/usr/bin/python

DOCUMENTATION = '''
name: panos_op_policy_match_result_to_bool
short_description: Evaluate policy match command result
description:
  - Evaluates the output of the 'test security-policy-match' command.
  - Returns true if there is already a matching policy, or false otherwise.
  - Handles both single results and lists of results.
version_added: "1.0.0"
author:
  - PaloAlto Networks (@PaloAltoNetworks)
options:
  _input:
    description:
      - Dictionary or list of dictionaries from panos_op command results
    type: raw
    required: true
'''

EXAMPLES = '''
# Check if security policy match found a result
- name: Set Test XML
  ansible.builtin.set_fact:
    policy_creation_test_xml: |
      <test>
        <security-policy-match>
          <source>10.10.11.1</source>
          <destination>8.8.8.8</destination>
          <application>{{ policy_creation_application | default('ssl') }}</application>
          <protocol>6</protocol>
          <destination-port>443</destination-port>
        </security-policy-match>
      </test>
      
- name: Test the current status of the security policy
  paloaltonetworks.panos.panos_op:
    provider:
      ip_address: "{{ provider.ip_address }}"
      username: "{{ provider.username }}"
      password: "{{ provider.password }}"
      serial_number: "{{ item.serial }}"
    cmd: "{{ policy_creation_test_xml }}"
    cmd_is_xml: true
  register: policy_creation_security_policy_match_result
  
- name: Set the policy match result
  ansible.builtin.set_fact:
    policy_creation_security_matches_existing_policy: >
      {{ policy_creation_security_policy_match_result |
         paloaltonetworks.panos_policy_automation.panos_op_policy_match_result_to_bool }}

'''

RETURN = '''
_value:
  description: True if a matching policy was found, False otherwise
  type: bool
  returned: always
'''

import json
from json import JSONDecodeError
from typing import Union


def panos_op_policy_match_result_to_bool(data):
    """Evaluates the output of the test-security policy match command, returning true if there is already a
    matching policy, or false otherwise."""
    if isinstance(data, dict):
        data = [data]

    for op_result in data:
        stdout = op_result.get("stdout")
        if stdout:
            try:
                stdout = json.loads(stdout)
            except JSONDecodeError:
                return False
            if stdout.get("response").get("result"):
                return True

    return False


class FilterModule(object):
    def filters(self):
        return {
            'panos_op_policy_match_result_to_bool': panos_op_policy_match_result_to_bool
        }