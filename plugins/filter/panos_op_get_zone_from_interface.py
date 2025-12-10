#!/usr/bin/python

DOCUMENTATION = '''
name: panos_op_get_zone_from_interface
short_description: Get security zone from interface names
description:
  - Looks up the output of the 'show interface all' command, mapping the given interface names to their zones.
  - Parses the XML output to ensure all different types of interfaces are captured.
version_added: "1.0.0"
author:
  - PaloAlto Networks (@PaloAltoNetworks)
options:
  _input:
    description:
      - Dictionary containing stdout_xml field from 'show interface all' command
    type: dict
    required: true
  interface_names:
    description:
      - List of interface names to look up zones for
    type: list
    elements: str
    required: true
'''

EXAMPLES = '''
# Get all the interfaces output
- name: Get the zone
  paloaltonetworks.panos.panos_op:
    provider:
      ip_address: "{{ provider.ip_address }}"
      username: "{{ provider.username }}"
      password: "{{ provider.password }}"
      serial_number: "{{ item.serial }}"
    cmd: "show interface all"
  register: interface_data

# Example with show interface all output
- name: Map interfaces to zones
  set_fact:
    zones: "{{ interface_data | panos_op_get_zone_from_interface(my_interfaces) }}"
  vars:
    my_interfaces:
      - ethernet1/1
      - ethernet1/2
'''

RETURN = '''
_value:
  description: List of zone names corresponding to the input interfaces
  type: list
  elements: str
  returned: always
'''

from xml.etree.ElementTree import fromstring
from typing import Union


def panos_op_get_zone_from_interface(data, interface_names):
    """Looks up the output of the `show interface all` command, mapping the given interface_name to the zone.
    Note this parses the XML to ensure we capture all the different types of interfaces.
    """
    zones = []
    xml_data = fromstring(data.get("stdout_xml"))
    entries = xml_data.findall(".//entry")
    for entry in entries:
        name = entry.find("name")
        if name is not None:
            if name.text in interface_names:
                zone = entry.find("zone")
                if zone is not None:
                    zones.append(zone.text)

    return zones


class FilterModule(object):
    def filters(self):
        return {
            'panos_op_get_zone_from_interface': panos_op_get_zone_from_interface
        }