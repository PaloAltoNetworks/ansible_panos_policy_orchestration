# Playbook Examples

These examples show how you might utilize the roles provided by this collection
in your own playbooks. You can, also, use them directly if you so choose.

The policy files specified by `policy_creation_policy_files` are relative paths
to the directory in which `ansible-playbook` is being executed.

## paloaltonetworks.panos_policy_automation.examples.lookup_policy

Performs a lookup in the security policy based on the given data.

### Example Vars File
```yaml
---
policy_creation_source_ip: 110.33.122.75
policy_creation_destination_ip: 10.10.10.5
lookup_policy_application: ssh
policy_creation_policy_files:
  - example_outbound_policy_file.yml
  - example_web_to_database_policy_file.yml
```

### Usage

```shell
ansible-playbook -i inventory_real.yml --extra-vars=@./example_vars_file_trusted_outbound.yml paloaltonetworks.panos_policy_automation.examples.lookup_policy
```

## paloaltonetworks.panos_policy_automation.examples.new_policy

Creates new policies or adds objects to existing groups based on their preset policy matches.

### Example Vars File
```yaml
---
policy_creation_source_ip: 110.33.122.75
policy_creation_destination_ip: 10.10.10.5
lookup_policy_application: ssh
policy_creation_policy_files:
  - example_outbound_policy_file.yml
  - example_web_to_database_policy_file.yml
```

### Usage

```shell
ansible-playbook -i inventory_real.yml --extra-vars=@./example_vars_file_trusted_outbound.yml paloaltonetworks.panos_policy_automation.examples.new_policy
```
