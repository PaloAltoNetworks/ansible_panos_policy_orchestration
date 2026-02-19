# lookup_policy Role

## Purpose
The `lookup_policy` role tests whether network traffic is permitted or denied by existing PAN-OS security policies. It provides policy validation capabilities that can be used standalone or as part of larger automation workflows.

## Overview
This role executes the `test security-policy-match` command against PAN-OS firewalls to determine if specified traffic would be allowed or blocked by current security policies. It's particularly useful for:

- **Pre-change validation** - Test if traffic is already permitted before creating new policies
- **Policy verification** - Validate that security policies work as expected
- **Compliance testing** - Ensure traffic flows match security requirements
- **Troubleshooting** - Determine why traffic might be blocked

## How it Works

The role follows this execution flow:

1. **Populates defaults** - Sets default values for destination port, protocol, and application
2. **Determines device group** - Sets the operating device group from variables
3. **Gets connected devices** - Retrieves list of all firewalls connected to Panorama (or uses specified serial)
4. **Tests security policies** - Runs security-policy-match tests against each device
5. **Returns result** - Sets a boolean variable indicating if traffic is permitted

## Role Variables

See [argument_specs.yml](../../roles/lookup_policy/meta/argument_specs.yml) for all variables with detailed descriptions.

### Required Variables

| Variable | Type | Description |
|----------|------|-------------|
| `policy_creation_source_ip` | str | Source IP address for policy testing |
| `policy_creation_destination_ip` | str | Destination IP address for policy testing |
| `provider` | dict | PAN-OS connection details (ip_address, username, password) |

### Optional Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `lookup_policy_destination_port` | str | `443` | TCP or UDP port used by the traffic |
| `lookup_policy_protocol` | str | `6` | IP protocol number (6=TCP, 17=UDP) |
| `lookup_policy_application` | str | `ssl` | PAN-OS compatible application name |
| `policy_creation_device_group` | str | N/A | Target device group for testing |
| `default_new_policy_device_group` | str | N/A | Fallback device group |
| `default_test_policy_serial_number` | str | N/A | Specific firewall serial for testing |

### Generated Variables

| Variable | Description |
|----------|-------------|
| `lookup_policy_security_matches_existing_policy` | Boolean indicating if traffic is permitted by existing policies |

## Requirements

- Python 3.11+
- Ansible 2.16+
- PAN-OS Ansible collection (`paloaltonetworks.panos`)
- panos_policy_automation collection (for filter plugins)

## Dependencies

- `paloaltonetworks.panos` collection
- Access to Panorama with appropriate permissions
- Connected firewalls for policy testing

## Example Usage

### Standalone Usage

```yaml
- name: Test if DNS traffic is permitted
  hosts: panorama
  gather_facts: no
  roles:
    - role: paloaltonetworks.panos_policy_automation.lookup_policy
      vars:
        policy_creation_source_ip: "10.1.1.5/32"
        policy_creation_destination_ip: "8.8.8.8/32"
        lookup_policy_application: "dns"
        lookup_policy_destination_port: "53"
        provider:
          ip_address: "{{ panorama_ip }}"
          username: "{{ panorama_username }}"
          password: "{{ panorama_password }}"

- name: Display result
  hosts: panorama
  tasks:
    - debug:
        msg: "Traffic is {{ 'PERMITTED' if lookup_policy_security_matches_existing_policy else 'BLOCKED' }}"
```

### Usage with Conditional Actions

```yaml
- name: Check policy and take action
  hosts: panorama
  gather_facts: no
  roles:
    - role: paloaltonetworks.panos_policy_automation.lookup_policy
      vars:
        policy_creation_source_ip: "{{ source_ip }}"
        policy_creation_destination_ip: "{{ dest_ip }}"
        lookup_policy_application: "{{ app_name }}"
        provider: "{{ pan_provider }}"

- name: Create policy if traffic is blocked
  hosts: panorama
  tasks:
    - name: Alert that traffic is blocked
      debug:
        msg: "WARNING: Traffic from {{ source_ip }} to {{ dest_ip }} is currently blocked!"
      when: not lookup_policy_security_matches_existing_policy

    - name: Create new policy
      # Your policy creation tasks here
      when: not lookup_policy_security_matches_existing_policy
```

### Testing Multiple Scenarios

```yaml
- name: Test multiple traffic scenarios
  hosts: panorama
  gather_facts: no
  tasks:
    - name: Test web traffic
      include_role:
        name: paloaltonetworks.panos_policy_automation.lookup_policy
      vars:
        policy_creation_source_ip: "10.1.1.5/32"
        policy_creation_destination_ip: "8.8.8.8/32"
        lookup_policy_application: "web-browsing"
        lookup_policy_destination_port: "443"
        provider: "{{ pan_provider }}"

    - set_fact:
        web_traffic_allowed: "{{ lookup_policy_security_matches_existing_policy }}"

    - name: Test SSH traffic
      include_role:
        name: paloaltonetworks.panos_policy_automation.lookup_policy
      vars:
        policy_creation_source_ip: "10.1.1.5/32"
        policy_creation_destination_ip: "8.8.8.8/32"
        lookup_policy_application: "ssh"
        lookup_policy_destination_port: "22"
        provider: "{{ pan_provider }}"

    - set_fact:
        ssh_traffic_allowed: "{{ lookup_policy_security_matches_existing_policy }}"

    - debug:
        msg:
          - "Web traffic: {{ 'ALLOWED' if web_traffic_allowed else 'BLOCKED' }}"
          - "SSH traffic: {{ 'ALLOWED' if ssh_traffic_allowed else 'BLOCKED' }}"
```

## Workflow Details

1. **Variable Setup** - Role sets default values for any undefined optional variables
2. **Device Discovery** - Queries Panorama for connected firewalls or uses specified serial number
3. **Policy Testing** - Executes `test security-policy-match` command on each device
4. **Result Parsing** - Converts PAN-OS response to boolean value
5. **Fact Setting** - Stores result in `lookup_policy_security_matches_existing_policy`

## Device Selection Behavior

### All Devices (Default)
When `default_test_policy_serial_number` is NOT defined:
- Queries Panorama using `show devices connected`
- Tests against all connected firewalls
- Returns true if ANY device permits the traffic

### Specific Device
When `default_test_policy_serial_number` IS defined:
- Tests only the specified firewall
- Faster execution in large environments
- Useful when devices are known to have identical policies

## Important Notes

### Test Command Behavior
- The `test security-policy-match` command simulates traffic without actually sending it
- Tests against the currently committed configuration (not pending changes)
- Does not trigger policy counters or logs
- Respects all security policy rules including deny rules

### NAT Considerations
- The role assumes NAT is not in use, or that NAT won't affect the test results
- For NAT environments, test with post-NAT addresses
- Policy match tests use actual IP addresses, not NAT-translated addresses

### Multiple Devices
- When testing against multiple devices, if ANY device permits the traffic, the result is true
- This may not reflect the actual traffic path
- Consider using `default_test_policy_serial_number` to test specific devices

## Performance Considerations

In environments with many connected firewalls:
- Use `default_test_policy_serial_number` to limit testing to representative firewalls
- Testing all devices can be slow in large deployments
- Consider implementing device filtering logic based on device groups

## Common Use Cases

### Pre-Change Validation
Test before creating policies to avoid duplicates:
```yaml
- include_role:
    name: paloaltonetworks.panos_policy_automation.lookup_policy
  vars:
    # test variables

- name: Only create policy if needed
  # create policy tasks
  when: not lookup_policy_security_matches_existing_policy
```

### Policy Verification After Changes
Validate that new policies work as expected:
```yaml
- name: Create new policy
  # policy creation tasks

- name: Commit changes
  # commit tasks

- name: Verify policy works
  include_role:
    name: paloaltonetworks.panos_policy_automation.lookup_policy
  vars:
    # test variables

- assert:
    that: lookup_policy_security_matches_existing_policy
    fail_msg: "Policy creation failed - traffic still blocked!"
    success_msg: "Policy verified - traffic is now permitted"
```

### Compliance Testing
Ensure security policies match requirements:
```yaml
- name: Test that database traffic is blocked from DMZ
  include_role:
    name: paloaltonetworks.panos_policy_automation.lookup_policy
  vars:
    policy_creation_source_ip: "{{ dmz_network }}"
    policy_creation_destination_ip: "{{ database_server }}"
    lookup_policy_application: "mysql"
    provider: "{{ pan_provider }}"

- assert:
    that: not lookup_policy_security_matches_existing_policy
    fail_msg: "COMPLIANCE VIOLATION: DMZ can access database!"
    success_msg: "Compliance check passed - DMZ blocked from database"
```

## Troubleshooting

### Role reports traffic is permitted but actual traffic is blocked
- Check if changes are pending commit
- Verify you're testing the correct source/destination IPs
- Ensure the application name matches PAN-OS application database
- Check if NAT is translating addresses

### Role reports traffic is blocked but actual traffic works
- Verify the test is running against the correct firewall
- Check if intrazone traffic rules apply
- Ensure you're using post-NAT addresses if NAT is in use

### Role fails to connect to devices
- Verify Panorama connectivity
- Check that firewalls are connected to Panorama
- Ensure credentials have appropriate permissions
- Verify device group exists

## Related Documentation

- [security_policy_match.md](security_policy_match.md) - Underlying task that performs policy testing
- [policy_creation_role.md](policy_creation_role.md) - Related role that creates policies
- [User Guide: Policy Validation](../user_guide/policy_validation.md) - How to use this role effectively

## See Also

- [Role README](../../roles/lookup_policy/README.md)
- [Argument Specifications](../../roles/lookup_policy/meta/argument_specs.yml)
- [PAN-OS test security-policy-match Documentation](https://docs.paloaltonetworks.com/)
