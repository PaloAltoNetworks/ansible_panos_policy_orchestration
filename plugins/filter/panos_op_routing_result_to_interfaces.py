
DOCUMENTATION = '''
name: panos_op_routing_result_to_interfaces
short_description: Extract interfaces from routing test command output
description:
  - Takes the output of the 'test routing' command and returns the interfaces.
  - Extracts interface information from the routing test results.
  - Handles both single results and lists of results.
version_added: "1.0.0"
author:
  - PaloAlto Networks (@PaloAltoNetworks)
options:
  _input:
    description:
      - Dictionary or list of dictionaries from panos_op routing test command results
    type: raw
    required: true
'''

EXAMPLES = '''

- name: Run a Fib lookup
  paloaltonetworks.panos.panos_op:
    provider:
      ip_address: "{{ provider.ip_address }}"
      username: "{{ provider.username }}"
      password: "{{ provider.password }}"
      serial_number: "{{ serialno }}"
    cmd: "<test><routing><fib-lookup><virtual-router>default</virtual-router><ip>8.8.8.8</ip></fib-lookup></routing></test>"
    cmd_is_xml: true
  register: lookup_policy__test_routing_result

- name: Get interfaces from results
  ansible.builtin.set_fact:
    lookup_policy_interface_list: >
      {{ lookup_policy__test_routing_result.results |
         paloaltonetworks.panos_policy_automation.panos_op_routing_result_to_interfaces }}
'''

RETURN = '''
_value:
  description: List of interface names from routing test results
  type: list
  elements: str
  returned: always
'''

import json


def panos_op_routing_result_to_interfaces(results):
    """Takes the output of the test routing command and returns the interfaces"""
    if isinstance(results, dict):
        results = [results]

    interfaces = []
    for result in results:
        data = json.loads(result.get("stdout"))
        interface = data.get("response").get("result").get("interface")
        interfaces.append(interface)

    return interfaces


class FilterModule(object):
    def filters(self):
        return {
            'panos_op_routing_result_to_interfaces': panos_op_routing_result_to_interfaces
        }
