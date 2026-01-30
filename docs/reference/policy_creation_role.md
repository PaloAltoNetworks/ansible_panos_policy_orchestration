# policy_creation Role

## Purpose
The `policy_creation` role automates the creation and management of security policies in Palo Alto Networks Panorama. It intelligently handles both preset policy updates (adding to existing groups) and new policy creation when no preset policies match.

## Overview
This role provides two main workflows:

1. **Preset Policy Updates** - Automatically updates existing, pre-built policies by adding addresses, applications, or URLs to existing groups
2. **New Policy Creation** - Creates entirely new security policies with automatic zone detection and policy validation

## How it Works

The role follows this execution flow:

1. **Preset Policy Evaluation** - Includes user-provided policy task files to test against preset policies
2. **Preset Updates** - If a preset policy matches, updates the relevant groups (addresses, applications, URLs)
3. **Policy Lookup** - If no preset matches, tests if traffic is already permitted and calculates zones
4. **New Policy Creation** - If traffic is not permitted, creates a new security policy
5. **Commit & Push** - Commits changes to Panorama and pushes to device groups
6. **Validation** - Tests the changes to ensure traffic is now permitted

## Role Variables

See [argument_specs.yml](../../roles/policy_creation/meta/argument_specs.yml) for all variables with detailed descriptions.

### Required Variables

| Variable | Type | Description |
|----------|------|-------------|
| `policy_creation_policy_files` | list | List of policy files containing preset policy tasks to evaluate |

### Optional Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `source_user` | str | N/A | Source user for the new policy |
| `policy_creation_source_ip` | str | N/A | Source IP address or CIDR block |
| `policy_creation_destination_ip` | str | N/A | Destination IP address or CIDR block |
| `lookup_policy_application` | str | `ssl` | PAN-OS compatible application name |
| `lookup_policy_destination_port` | str | `443` | TCP or UDP port used by the traffic |

### Common Additional Variables

These variables are commonly used but not defined in argument_specs (referenced in tasks):

| Variable | Description | Default |
|----------|-------------|---------|
| `provider` | PAN-OS connection details (ip_address, username, password) | Required |
| `policy_creation_device_group` | Target device group for policy creation | N/A |
| `default_new_policy_device_group` | Fallback device group | N/A |
| `default_new_policy_tag` | Tag to apply to auto-created policies | N/A |
| `default_rule_location` | Where to place new rules (before/after) | N/A |
| `default_location_rule_name` | Reference rule for positioning new rules | N/A |
| `default_test_policy_serial_number` | Specific firewall serial for testing | N/A |

### Generated Variables

| Variable | Description |
|----------|-------------|
| `policy_creation_config_changed` | Boolean indicating if any configuration changes were made |
| `policy_creation_policy_match` | Boolean indicating if a preset policy matched |
| `lookup_policy_security_matches_existing_policy` | Boolean indicating if traffic is already permitted |

## Task File Reference

The role is organized into several task files, each handling specific functionality:

### Main Entry Point
- **[main.yml](../../roles/policy_creation/tasks/main.yml)** - Orchestrates all workflows

### New Policy Creation Tasks (tasks/new/)
- **[lookup_policy.md](lookup_policy.md)** - Tests security policies and calculates zones
- **[security_policy_match.md](security_policy_match.md)** - Runs test security-policy-match commands
- **[get_zone_by_ip.md](get_zone_by_ip.md)** - Determines zones from routing tables
- **[create_policy.md](create_policy.md)** - Creates new security policies

### Preset Policy Tasks (tasks/preset/)
- **[add_address_to_preset_group.md](add_address_to_preset_group.md)** - Adds addresses to existing address groups
- **[add_application_to_preset_group.md](add_application_to_preset_group.md)** - Adds applications to existing application groups
- **[add_url_to_preset_category.md](add_url_to_preset_category.md)** - Adds URLs to existing custom URL categories

## Requirements

- Python 3.11+
- Ansible 2.16+
- PAN-OS Ansible collection (`paloaltonetworks.panos`)
- panos_policy_automation collection (for filter plugins)

## Dependencies

- `paloaltonetworks.panos` collection
- Access to Panorama with appropriate permissions
- Connected firewalls for zone discovery and policy testing

## Example Usage

```yaml
- name: Create or update security policy
  hosts: panorama
  gather_facts: yes
  roles:
    - role: paloaltonetworks.panos_policy_automation.policy_creation
      vars:
        policy_creation_policy_files:
          - preset_policies/webserver_outbound.yml
        policy_creation_source_ip: "10.1.1.5/32"
        policy_creation_destination_ip: "8.8.8.8/32"
        lookup_policy_application: "dns"
        lookup_policy_destination_port: "53"
        provider:
          ip_address: "{{ panorama_ip }}"
          username: "{{ panorama_username }}"
          password: "{{ panorama_password }}"
        default_new_policy_device_group: "Branch-Offices"
        default_new_policy_tag: "automated"
```

## Workflow Details

### Preset Policy Workflow
1. Role includes each file in `policy_creation_policy_files`
2. Each file tests if the request matches its preset policy criteria
3. If matched, sets `policy_creation_policy_match: true` and defines group variables
4. Role updates the relevant groups (addresses, applications, URLs)
5. Changes are committed and pushed to device groups

### New Policy Workflow
1. Triggers when `policy_creation_policy_match` is false
2. Retrieves all connected devices from Panorama
3. Tests traffic against existing policies on each device
4. If traffic is not permitted:
   - Performs routing table lookups to determine destination zones
   - Creates address objects for source and destination IPs
   - Creates a new security rule with calculated or default zones
5. Commits and pushes changes
6. Validates that traffic is now permitted

## Notes

- Zone detection queries all firewalls connected to Panorama by default
- Use `default_test_policy_serial_number` to limit testing to a specific firewall
- New policies are auto-named as `autogen_<timestamp>`
- Address objects are auto-named as `addr_<ip_sanitized>`
- All automation-created rules are tagged for easy identification
- The role handles both legacy routing tables and advanced routing

## See Also

- [Role README](../../roles/policy_creation/README.md)
- [User Guide: New Policy Creation](../user_guide/new_policy_creation.md)
- [User Guide: Preset Policies](../user_guide/preset_policy.md)
