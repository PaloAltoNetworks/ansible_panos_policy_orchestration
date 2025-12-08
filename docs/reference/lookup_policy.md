# lookup_policy.yml

## Purpose
Tests existing security policies to determine if traffic is already permitted and calculates zones for new policy creation. This is the primary analysis tasks file that determines whether new policies are needed.

## What it does
1. **Populates defaults** - Sets default values for destination port, protocol, and application
2. **Determines device group** - Sets the operating device group from variables
3. **Gets connected devices** - Retrieves list of all firewalls connected to Panorama (or uses specified serial)
4. **Tests security policies** - Runs security-policy-match tests against each device
5. **Calculates destination zones** - Determines appropriate zones based on routing tables

## Required Variables

| Variable | Description |
|----------|-------------|
| `policy_creation_source_ip` | Source IP address for policy testing |
| `policy_creation_destination_ip` | Destination IP address for policy testing |
| `provider` | PAN-OS connection details (ip_address, username, password) |

## Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `policy_creation_destination_port` | Destination port for testing | `443` |
| `policy_creation_protocol` | IP protocol number | `6` (TCP) |
| `application` | Application for testing | `ssl` |
| `device_group` | Target device group | N/A |
| `default_new_policy_device_group` | Fallback device group | N/A |
| `default_test_policy_serial_number` | Specific firewall serial for testing | N/A |

## Generated Variables

| Variable | Description |
|----------|-------------|
| `policy_creation_security_matches_existing_policy` | Boolean indicating if traffic is already permitted |
| `destination_zones` | List of calculated destination zones |

## Dependencies
- Requires PAN-OS collection
- Includes `security_policy_match.yml` for policy testing
- Includes `get_zone_by_ip.yml` for zone calculation
- Must have either `device_group` or `default_new_policy_device_group` defined