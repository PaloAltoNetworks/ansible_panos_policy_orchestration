
DOCUMENTATION = '''
name: panos_op_stdout_results_to_list
short_description: Convert panos_op results to list of stdout data
description:
  - Takes a list of result dictionaries of command results for panos_op and returns a list of all the stdout data.
  - Useful when you have multiple panos_op command results and want to extract just the stdout content.
version_added: "1.0.0"
author:
  - PaloAlto Networks (@PaloAltoNetworks)
options:
  _input:
    description:
      - List or single dictionary of panos_op command results
    type: raw
    required: true
'''

EXAMPLES = '''
# Convert multiple panos_op results to list
- name: Extract stdout from multiple op results
  set_fact:
    stdout_list: "{{ op_results | panos_op_stdout_results_to_list }}"

# Example with actual data
- name: Parse multiple command outputs
  set_fact:
    parsed_outputs: "{{ command_results | panos_op_stdout_results_to_list }}"
  vars:
    command_results:
      - stdout: '{"response": {"result": "data1"}}'
      - stdout: '{"response": {"result": "data2"}}'
'''

RETURN = '''
_value:
  description: List of parsed JSON objects from stdout fields
  type: list
  returned: always
'''

import json


def panos_op_stdout_results_to_list(data):
    """Takes a list of result dictionaries of command results for panos_op and returns a list of all the
    stdout data instead"""
    result = []
    if isinstance(data, dict):
        data = [data]
    for op_result in data:
        if op_result.get("stdout"):
            result.append(json.loads(op_result.get("stdout")))

    return result


class FilterModule(object):
    def filters(self):
        return {
            'panos_op_stdout_results_to_list': panos_op_stdout_results_to_list
        }
