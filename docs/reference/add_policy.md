# add_policy.yml

## Purpose
Main orchestrator tasks file that coordinates the entire security policy workflow. Handles both preset policy updates and new policy creation, with automatic commit and push operations.

## What it does
1. **Preset policy matching** - Tests against pre-configured policy templates
2. **Preset updates** - Updates existing address groups and application groups when policies match
3. **New policy creation** - Creates entirely new policies when no presets match
4. **Configuration commit** - Commits and pushes changes to device groups
5. **Validation** - Re-tests policies after creation to verify success

## Required Variables

| Variable | Description |
|----------|-------------|
| `source_ip` | Source IP address for the policy |
| `destination_ip` | Destination IP address for the policy |
| `provider` | PAN-OS connection details (ip_address, username, password) |

## Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `device_group` | Target device group | `default_new_policy_device_group` |
| `source_address_group` | Preset source address group | N/A |
| `destination_address_group` | Preset destination address group | N/A |
| `application_group` | Preset application group | N/A |
| `application` | Application name | N/A |

## Generated Variables

| Variable | Description |
|----------|-------------|
| `policy_creation_config_changed` | Boolean indicating if configuration was modified |
| `policy_match` | Boolean indicating if traffic matched a preset policy |
| `matches_existing_policy` | Boolean from policy testing results |

## Dependencies
- Requires PAN-OS collection
- Includes multiple preset policy files:
  - `preset/webservers_outbound_policy.yml`
  - `preset/ssh_jumpserver_inbound_access.yml`
  - `preset/add_address_to_preset_group.yml`
  - `preset/add_application_to_preset_group.yml`
- Includes new policy creation files:
  - `new/lookup_policy.yml`
  - `new/create_policy.yml`
- Requires either `device_group` or `default_new_policy_device_group` to be defined