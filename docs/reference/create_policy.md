# create_policy.yml

## Purpose
Creates a new security policy with auto-generated address objects and rule placement. This tasks file is executed when no existing preset policies match the traffic requirements.

## What it does
1. **Populates defaults** - Sets default values for zones, tags, rule names, and device groups
2. **Creates tag object** - Creates or ensures the policy tag exists in the shared device group
3. **Creates address objects** - Auto-generates address objects for both source and destination IPs
4. **Creates security rule** - Creates the actual security policy rule with proper positioning

## Required Variables

| Variable | Description |
|----------|-------------|
| `source_ip` | Source IP address or CIDR block |
| `destination_ip` | Destination IP address or CIDR block |
| `application` | Application name for the rule |
| `provider` | PAN-OS connection details (ip_address, username, password) |

## Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `source_zones` | Source zones | `['any']` |
| `destination_zones` | Destination zones | `['any']` |
| `tag` | Policy tag | `default_new_policy_tag` |
| `device_group` | Target device group | `default_new_policy_device_group` |
| `default_rule_location` | Rule placement | N/A |
| `default_location_rule_name` | Reference rule for positioning | N/A |

## Generated Variables

| Variable | Description |
|----------|-------------|
| `rule_name` | Auto-generated as `autogen_<timestamp>` |
| `source_address_name` | Auto-generated as `addr_<source_ip_sanitized>` |
| `destination_address_name` | Auto-generated as `addr_<destination_ip_sanitized>` |
| `policy_created` | Set to the created rule name |
| `policy_creation_config_changed` | Set to `true` |

## Dependencies
- Requires PAN-OS collection
- Must be called after zone discovery (if using auto-calculated zones)