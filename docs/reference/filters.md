# Filter Plugins

This collection provides several custom Ansible filter plugins for parsing and manipulating PAN-OS operational command output. These filters make it easier to work with data returned from the `paloaltonetworks.panos.panos_op` module.

## Available Filters

- [panos_op_stdout_to_dict](#panos_op_stdout_to_dict) - Convert panos_op stdout to dictionary
- [panos_op_stdout_results_to_list](#panos_op_stdout_results_to_list) - Convert multiple panos_op results to list
- [panos_op_policy_match_result_to_bool](#panos_op_policy_match_result_to_bool) - Evaluate policy match command results
- [panos_op_get_zone_from_interface](#panos_op_get_zone_from_interface) - Get security zones from interface names
- [panos_op_routing_result_to_interfaces](#panos_op_routing_result_to_interfaces) - Extract interfaces from routing test output
- [panos_op_get_routers_from_dict_or_list](#panos_op_get_routers_from_dict_or_list) - Extract router names from routing table

---

## panos_op_stdout_to_dict

**Plugin Path:** `plugins/filter/panos_op_stdout_to_dict.py`

### Purpose
Converts the stdout field from a `panos_op` command result to a parsed dictionary, making it easier to manipulate JSON output from PAN-OS operational commands.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `_input` | dict | Yes | The result dictionary from panos_op command containing stdout field |

### Returns
- **Type:** dict
- **Description:** Parsed dictionary from stdout JSON

### Example Usage

```yaml
- name: Get all connected devices
  paloaltonetworks.panos.panos_op:
    provider: "{{ provider }}"
    cmd: "show devices connected"
  register: lookup_policy__show_devices_output

- name: Convert stdout to dictionary
  ansible.builtin.set_fact:
    devices_dict: >
      {{ lookup_policy__show_devices_output |
         paloaltonetworks.panos_policy_automation.panos_op_stdout_to_dict }}

- name: Access parsed data
  debug:
    msg: "Device count: {{ devices_dict.response.result.devices | length }}"
```

### Error Handling
Raises `PanosStdoutParseError` if stdout contains invalid JSON.

### Used In
- `roles/policy_creation/tasks/new/lookup_policy.yml:16` - Parsing device list
- `roles/policy_creation/tasks/new/get_zone_by_ip.yml:21` - Parsing routing table

---

## panos_op_stdout_results_to_list

**Plugin Path:** `plugins/filter/panos_op_stdout_results_to_list.py`

### Purpose
Takes a list of panos_op command results and extracts just the stdout data as parsed JSON objects. Useful when processing multiple command outputs.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `_input` | raw (dict or list) | Yes | Single dictionary or list of dictionaries from panos_op commands |

### Returns
- **Type:** list
- **Description:** List of parsed JSON objects from stdout fields

### Example Usage

```yaml
- name: Run commands on multiple devices
  paloaltonetworks.panos.panos_op:
    provider: "{{ provider }}"
    cmd: "show system info"
    serial_number: "{{ item }}"
  loop: "{{ device_serials }}"
  register: system_info_results

- name: Extract just the stdout data
  ansible.builtin.set_fact:
    system_info_list: >
      {{ system_info_results.results |
         paloaltonetworks.panos_policy_automation.panos_op_stdout_results_to_list }}

- name: Process each result
  debug:
    msg: "Hostname: {{ item.response.result.system.hostname }}"
  loop: "{{ system_info_list }}"
```

### Behavior
- Accepts both single dictionary and list of dictionaries
- Filters out results without stdout field
- Parses each stdout field as JSON
- Returns list of parsed objects

---

## panos_op_policy_match_result_to_bool

**Plugin Path:** `plugins/filter/panos_op_policy_match_result_to_bool.py`

### Purpose
Evaluates the output of the `test security-policy-match` command and returns true if a matching policy exists, false otherwise.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `_input` | raw (dict or list) | Yes | Dictionary or list of dictionaries from panos_op security-policy-match results |

### Returns
- **Type:** bool
- **Description:** True if a matching policy was found, False otherwise

### Example Usage

```yaml
- name: Set test XML
  ansible.builtin.set_fact:
    test_xml: |
      <test>
        <security-policy-match>
          <source>10.10.11.1</source>
          <destination>8.8.8.8</destination>
          <application>ssl</application>
          <protocol>6</protocol>
          <destination-port>443</destination-port>
        </security-policy-match>
      </test>

- name: Test security policy
  paloaltonetworks.panos.panos_op:
    provider: "{{ provider }}"
    serial_number: "{{ device_serial }}"
    cmd: "{{ test_xml }}"
    cmd_is_xml: true
  register: policy_match_result

- name: Evaluate result
  ansible.builtin.set_fact:
    traffic_permitted: >
      {{ policy_match_result |
         paloaltonetworks.panos_policy_automation.panos_op_policy_match_result_to_bool }}

- name: Display result
  debug:
    msg: "Traffic is {{ 'ALLOWED' if traffic_permitted else 'BLOCKED' }}"
```

### Behavior
- Handles both single result dictionary and list of results
- Returns true if ANY result indicates a policy match
- Returns false if no results or all results indicate no match
- Gracefully handles JSON decode errors (returns false)

### Used In
- `roles/policy_creation/tasks/new/security_policy_match.yml:30` - Determining if new policy is needed
- `roles/lookup_policy/tasks/main.yml` - Policy validation

---

## panos_op_get_zone_from_interface

**Plugin Path:** `plugins/filter/panos_op_get_zone_from_interface.py`

### Purpose
Maps interface names to their assigned security zones by parsing the output of the `show interface all` command.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `_input` | dict | Yes | Dictionary containing stdout_xml field from 'show interface all' command |
| `interface_names` | list[str] | Yes | List of interface names to look up zones for |

### Returns
- **Type:** list[str]
- **Description:** List of zone names corresponding to the input interfaces

### Example Usage

```yaml
- name: Get all interfaces
  paloaltonetworks.panos.panos_op:
    provider: "{{ provider }}"
    serial_number: "{{ device_serial }}"
    cmd: "show interface all"
  register: interface_data

- name: Map interfaces to zones
  ansible.builtin.set_fact:
    zones: >
      {{ interface_data |
         paloaltonetworks.panos_policy_automation.panos_op_get_zone_from_interface(target_interfaces) }}
  vars:
    target_interfaces:
      - ethernet1/1
      - ethernet1/2

- name: Display zones
  debug:
    msg: "Interfaces map to zones: {{ zones }}"
```

### Behavior
- Parses XML output to capture all interface types (ethernet, aggregate, tunnel, etc.)
- Returns zones in the same order as input interface names
- Only includes zones for interfaces that have zone assignments
- Interfaces without zones are omitted from results

### Used In
- `roles/policy_creation/tasks/new/get_zone_by_ip.yml:69` - Zone discovery for policy creation

---

## panos_op_routing_result_to_interfaces

**Plugin Path:** `plugins/filter/panos_op_routing_result_to_interfaces.py`

### Purpose
Extracts interface names from the output of the `test routing fib-lookup` command.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `_input` | raw (dict or list) | Yes | Dictionary or list of dictionaries from panos_op routing test results |

### Returns
- **Type:** list[str]
- **Description:** List of interface names from routing test results

### Example Usage

```yaml
- name: Run FIB lookup
  paloaltonetworks.panos.panos_op:
    provider: "{{ provider }}"
    serial_number: "{{ device_serial }}"
    cmd: |
      <test>
        <routing>
          <fib-lookup>
            <virtual-router>default</virtual-router>
            <ip>8.8.8.8</ip>
          </fib-lookup>
        </routing>
      </test>
    cmd_is_xml: true
  register: fib_result

- name: Extract interface
  ansible.builtin.set_fact:
    egress_interface: >
      {{ fib_result |
         paloaltonetworks.panos_policy_automation.panos_op_routing_result_to_interfaces }}

- name: Display routing decision
  debug:
    msg: "Traffic to 8.8.8.8 exits via: {{ egress_interface }}"
```

### Behavior
- Accepts both single result and list of results
- Parses JSON stdout from each result
- Extracts the interface field from routing test response
- Returns list of interface names

### Used In
- `roles/policy_creation/tasks/new/get_zone_by_ip.yml:56` - Determining egress interfaces for zone calculation

---

## panos_op_get_routers_from_dict_or_list

**Plugin Path:** `plugins/filter/panos_op_get_routers_from_dict_or_list.py`

### Purpose
Returns a list of logical router names from the output of the `show advanced-routing route` command. Specifically designed for advanced routing engine (ARE) output.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `_input` | raw | Yes | Dictionary output from show advanced-routing route command |

### Returns
- **Type:** list[str]
- **Description:** List of logical router names

### Example Usage

```yaml
- name: Get advanced routing table
  paloaltonetworks.panos.panos_op:
    provider: "{{ provider }}"
    serial_number: "{{ device_serial }}"
    cmd: "<show><advanced-routing><route/></advanced-routing></show>"
    cmd_is_xml: true
  register: routing_table

- name: Extract router names
  ansible.builtin.set_fact:
    logical_routers: >
      {{ routing_table |
         paloaltonetworks.panos_policy_automation.panos_op_get_routers_from_dict_or_list }}

- name: Display routers
  debug:
    msg: "Found routers: {{ logical_routers }}"
```

### Behavior
- Designed for PAN-OS advanced routing engine (ARE) output
- ARE results are embedded as JSON within XML response
- Extracts router names from JSON data structure
- Returns empty list if no JSON data found

### Used In
- `roles/policy_creation/tasks/new/get_zone_by_ip.yml:32` - Getting virtual routers for FIB lookups

### Version Compatibility
- Works with PAN-OS versions using advanced routing engine
- For legacy routing, use standard routing commands (handled by role logic)

---

## Common Patterns

### Chaining Filters

Filters can be chained together for complex data transformations:

```yaml
- name: Get devices and extract specific data
  ansible.builtin.set_fact:
    device_hostnames: >
      {{ devices_output |
         panoaltonetworks.panos_policy_automation.panos_op_stdout_to_dict |
         json_query('response.result.devices[*].hostname') }}
```

### Error Handling

Most filters gracefully handle missing data:

```yaml
- name: Safe parsing with default
  ansible.builtin.set_fact:
    zones: >
      {{ interface_data |
         paloaltonetworks.panos_policy_automation.panos_op_get_zone_from_interface(interfaces) |
         default(['any']) }}
```

### Loop Processing

Filters work well with loops:

```yaml
- name: Test routing on multiple routers
  paloaltonetworks.panos.panos_op:
    provider: "{{ provider }}"
    cmd: "<test><routing><fib-lookup><virtual-router>{{ item }}</virtual-router><ip>{{ target_ip }}</ip></fib-lookup></routing></test>"
    cmd_is_xml: true
  loop: "{{ virtual_routers }}"
  register: fib_results

- name: Get all egress interfaces
  ansible.builtin.set_fact:
    all_interfaces: >
      {{ fib_results.results |
         paloaltonetworks.panos_policy_automation.panos_op_routing_result_to_interfaces |
         unique }}
```

## Requirements

All filter plugins require:
- Python 3.11+
- Ansible 2.16+
- PAN-OS Ansible collection (`paloaltonetworks.panos`)

## See Also

- [policy_creation_role.md](policy_creation_role.md) - Role that uses these filters
- [lookup_policy_role.md](lookup_policy_role.md) - Role that uses these filters
- [PAN-OS Operational Commands](https://docs.paloaltonetworks.com/) - Documentation for underlying PAN-OS commands
