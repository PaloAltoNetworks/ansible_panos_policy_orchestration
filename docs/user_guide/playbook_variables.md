# Playbook Variables Reference

## Core Variables

### Required Variables

**`policy_creation_source_ip`** - Source IP address or CIDR block for the policy
- Example: `192.168.1.10` or `10.10.10.0/24`

**`policy_creation_destination_ip`** - Destination IP address or CIDR block for the policy
- Example: `8.8.8.8` or `203.0.113.0/24`

**`provider`** - PAN-OS connection details
- `ip_address` - Panorama IP address
- `username` - Authentication username
- `password` - Authentication password

### Optional Variables

**`application`** - Application name for the security rule
- Default: `ssl`
- Example: `ssh`, `dns`, `web-browsing`

**`policy_creation_destination_port`** - Destination port number
- Default: `443`
- Example: `22`, `53`, `80`

**`policy_creation_protocol`** - IP protocol number
- Default: `6` (TCP)
- Example: `17` (UDP), `1` (ICMP)

## Device and Group Configuration

**`device_group`** - Target device group for the policy
- Overrides `default_new_policy_device_group` when specified

**`default_new_policy_device_group`** - Default device group for new policies

**`default_test_policy_serial_number`** - Specific firewall serial number for testing
- When not specified, tests against all connected devices

## Preset Policy Variables

**`policy_creation_source_address_group`** - Existing address group to add source IP to
- Used for preset policy configurations

**`policy_creation_destination_address_group`** - Existing address group to add destination IP to
- Used for preset policy configurations

**`application_group`** - Existing application group to add application to
- Used for preset policy configurations

## Rule Creation Variables

**`tag`** - Tag to apply to created security rules
- Default: `default_new_policy_tag`

**`default_new_policy_tag`** - Default tag for new policies

**`default_rule_location`** - Rule placement location (`top`, `bottom`, `before`, `after`)

**`default_location_rule_name`** - Reference rule name for positioning when using `before` or `after`

## Zone Configuration

**`source_zones`** - List of source zones for the rule
- Default: `['any']`

**`destination_zones`** - List of destination zones for the rule
- Default: `['any']` or auto-calculated based on routing