import json

DOCUMENTATION = '''
name: panos_op_routers_from_dict_or_list
short_description: Returns a list of logical routers from the output of the 'show advanced-routing route' command.
description:
  - Returns a usable list of logical routers (by name) from the output of 'show-advanced-routing route'
version_added: "1.0.0"
author:
  - PaloAlto Networks (@PaloAltoNetworks)
options:
  _input:
    description:
      - Dictionary output of show advanced-routing route command
    type: raw
    required: true
'''

EXAMPLES = '''
- name: Get the ADVANCED ROUTING TABLE
  paloaltonetworks.panos.panos_op:
    provider:
      ip_address: "{{ provider.ip_address }}"
      username: "{{ provider.username }}"
      password: "{{ provider.password }}"
      serial_number: "{{ item.serial }}"
    cmd: "<show><advanced-routing><route/></advanced-routing></show>"
    cmd_is_xml: true
  register: result

- name: Parse and return the list of logical routers
  ansible.builtin.set_fact:
    logical_routers: >
        "{{ result | paloaltonetworks.panos_policy_automation.panos_op_get_routers_from_dict_or_list }}"
'''

RETURN = '''
_value:
  description: List of logical routers
  type: list
  elements: str
  returned: always
'''

from xml.etree.ElementTree import fromstring


def panos_op_get_routers_from_dict_or_list(data):
    """Looks up the output of the `show interface all` command, mapping the given interface_name to the zone.
    Note this parses the XML to ensure we capture all the different types of interfaces.
    """
    routers = []
    xml_data = fromstring(data.get("stdout_xml"))
    # ARE results are embedded as JSON in the XML
    json_data = xml_data.find("./result/json")
    if json_data is None:
        return routers

    data = json.loads(json_data.text)
    for router_name in data.keys():
        routers.append(router_name)

    return routers


class FilterModule(object):
    def filters(self):
        return {
            'panos_op_get_routers_from_dict_or_list': panos_op_get_routers_from_dict_or_list
        }
