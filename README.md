# Ansible PAN-OS Policy Automation

![GitHub commit activity](https://img.shields.io/github/commit-activity/w/adambaumeister/ansible_panos_policy_orchestration)
![GitHub commits difference between two branches/tags/commits](https://img.shields.io/github/commits-difference/paloaltonetworks/ansible_panos_policy_orchestration?base=master&head=develop&label=Changes%20Pending%20Release)
![Ansible Lint/Sanity Checks](https://img.shields.io/github/actions/workflow/status/paloaltonetworks/ansible_panos_policy_orchestration/ci.yml?label=Ansible%20Lint%2FSanity%20Checks)
![GitHub License](https://img.shields.io/github/license/adambaumeister/ansible_panos_policy_orchestration)
![GitHub Repo stars](https://img.shields.io/github/stars/adambaumeister/ansible_panos_policy_orchestration)
![GitHub Release](https://img.shields.io/github/v/release/adambaumeister/ansible_panos_policy_orchestration)
![Github Pages](https://img.shields.io/badge/github-pages-black?logo=githubpages&link=https%3A%2F%2Fadambaumeister.github.io%2Fansible_panos_policy_orchestration%2F)

[Documentation](https://paloaltonetworks.github.io/ansible_panos_policy_orchestration/)

This repository provides a framework and a philosophy for creating PAN-OS security policies
via Automation.

This repository would be of interest to you if:

 * You deal with a large number of incoming user requests for security policy
 * You can make repeatable, actionable policy decisions 
 * You are comfortable with Ansible or General automation platforms.

## Requirements

 * Python 3.11+
 * Ansible 2.16+
 * Panorama (this collection does NOT work for standalone firewalls or Strata Cloud Manager)
 * NGFWs connected to Panorama must be running Routed mode

## Installation

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:

```shell
ansible-galaxy install paloaltonetworks.panos_policy_automation
```

You can also include it in a requirements.yml file and install it with ansible-galaxy collection install -r requirements.yml, using the format:

```yaml
collections:
  - name: paloaltonetworks.panos_policy_automation
```

To upgrade the collection to the latest available version, run the following command:

```
ansible-galaxy collection install paloaltonetworks.panos_policy_automation --upgrade
```

You can also install a specific version of the collection. Use the following syntax to install version 1.0.0:

```
ansible-galaxy collection install paloaltonetworks.panos_policy_automation:==1.0.0
```

See [using Ansible collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

### Post-Installation Configuration

In this example, we are defining one panorama host under "lab".

```yaml title='inventory.yml'
all:
  children:
    # the `lab` group is included here as an example, but you can layout your panorama devices however you like.
    # Note you will need to create your own primary playbook mirroring `lab_policy.yml` if you change the grouping.
    lab:
      hosts:
        lab-panorama01:
          ansible_host: < YOUR PANORAMA HOSTNAME OR IP HERE >
          # Password should be provided via ANSIBLE_NET_PASSWORD environment variable
          # Example: export ANSIBLE_NET_PASSWORD="admin_password"
          
          # Username should be provided via ANSIBLE_NET_USERNAME environment variable
          # Example: export ANSIBLE_NET_USERNAME="admin"
      vars:
        # Common variables
        ansible_connection: local
        ansible_python_interpreter: "{{ ansible_playbook_python }}"
        # These variables are only used when creating COMPLETELY NEW policies
        default_new_policy_device_group: Lab
        default_new_policy_rulebase: post-rulebase
        default_new_policy_tag: AUTOMATED
        default_rule_location: bottom
```

### Define your preset policy files

Preset policy files are used to map incoming policy requests to object groups or security rules using Ansible filter
logic. Policy files are literal task files that produce the required variables for the role to execute.

Here's an example:

```yaml
---
# This is the Webservers outbound policy. The purpose of these tasks is to take incoming requests and see if they
# match this policy, returning the preset address group that they can be added to when a policy change is required.
# Webservers should be allowed to talk to any host on the internet, so we can disregard the destination IP!

- name: Match webserver outbound policy
  ansible.builtin.set_fact:
    policy_match: true # Set the fact that we did match a policy
    policy_creation_source_address_group: PRESET_LAB_WEB_OUTBOUND # In this case, the policy preset is an address_group type
    application_group: PRESET_LAB_WEB_OUTBOUND # If an application is passed, we should also include it in the policy.
    device_group: Lab # Finally, we set the device group!
  when:
    - policy_creation_source_ip is defined
    - policy_creation_destination_ip is defined
    - "'10.10.10.0/24' | ansible.utils.network_in_network( policy_creation_source_ip )"
    - "not '10.0.0.0/8' | ansible.utils.network_in_network( policy_creation_destination_ip )"
```

### Create the policy request, as an ansibles vars file

Now, we have to give Ansible variables for the new policy to define the attributes.

For simplicity, we do so within a vars file. 

```yaml
---
policy_creation_source_ip: 10.10.10.11
policy_creation_destination_ip: 8.8.8.8
application: dns
policy_creation_policy_files:
  - example_outbound_policy_file.yml  # <---- Note we included your "policy file" here!
```

Note, replace the playbook and vars file names with your versions.

```shell
ansible-playbook -i inventory.yml --extra-vars=@./policy_file.yml paloaltonetworks.panos_policy_automation.examples.create_policy
```

## Use Cases

**Automatically updating Object Groups**

Transforming requests for policy to new network objects.

**Automatically creating policy at preset locations**

Deploying new security rules to the bottom, top, or at a preset location such as "after this rule".

## Testing

This collection has been tested in lab environments with the following specs:

| product         | version                   |
|-----------------|---------------------------|
| Panorama        | 11.2.3-h3                 |
| vm-series       | 11.2.3-h3                 |
| mode            | routed                    |
| router type     | virtual (legacy, not ARE) |
| Total Firewalls | 1                         |


## Support

For support, please raise a [Github issue](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/issues. This collection is supported by PaloAltoNetworks on a **best effort basis**
only. For more detailed support, including deployment help, contact Palo Alto Networks Professional Services.

## Release Notes and Roadmap

View the [Releases](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/releases) page for a detailed
changelog.

## Related Information

Read the [docs](https://paloaltonetworks.github.io/ansible_panos_policy_orchestration/) for more information.

## License Information

[LICENSE.md](LICENSE.md)

## Responsible AI Assistance Disclosure

Generative AI, through the use of large language models, has been used selectively in this repository
in the following ways:

1. Creating or editing documentation
2. Refactoring modules (such as changing parent path)
3. Creation of unit tests

## Support
This Collection of Ansible Roles and Plugins is certified on Ansible Automation Hub and officially supported for Ansible
subscribers. Ansible subscribers can engage for support through their usual route towards Red Hat.

For those who are not Ansible subscribers, this Collection of Ansible Modules is also published on Ansible Galaxy to be
freely used under an as-is, best effort, support policy. These scripts should be seen as community supported and Palo 
Alto Networks will contribute our expertise as and when possible. We do not provide technical support or help in using 
or troubleshooting the components of the project through our normal support options such as Palo Alto Networks support 
teams, or ASC (Authorized Support Centers) partners and backline support options. The underlying product used 
(the VM-Series firewall) by the scripts or templates are still supported, but the support is only for the product 
functionality and not for help in deploying or using the template or script itself.

Unless explicitly tagged, all projects or work posted in our GitHub repository (at https://github.com/PaloAltoNetworks) 
or sites other than our official Downloads page on https://support.paloaltonetworks.com are provided under the best 
effort policy.