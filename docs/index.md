# Ansible PAN-OS Policy Automation

![GitHub commit activity](https://img.shields.io/github/commit-activity/w/adambaumeister/ansible_panos_policy_orchestration)
![GitHub commits difference between two branches/tags/commits](https://img.shields.io/github/commits-difference/adambaumeister/ansible_panos_policy_orchestration?base=master&head=develop&label=Changes%20Pending%20Release)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/adambaumeister/ansible_panos_policy_orchestration/ci.yml)
![GitHub License](https://img.shields.io/github/license/adambaumeister/ansible_panos_policy_orchestration)
![GitHub Repo stars](https://img.shields.io/github/stars/adambaumeister/ansible_panos_policy_orchestration)
![GitHub Release](https://img.shields.io/github/v/release/adambaumeister/ansible_panos_policy_orchestration)
![Github Pages](https://img.shields.io/badge/github-pages-black?logo=githubpages&link=https%3A%2F%2Fadambaumeister.github.io%2Fansible_panos_policy_orchestration%2F)

This repository provides a framework and a philosophy for creating PAN-OS security policies
via Automation.

This repository would be of interest to you if:

 * You deal with a large number of incoming user requests for security policy
 * You can make repeatable, actionable policy decisions 
 * You are comfortable with Ansible or General automation platforms.

## Quickstart

### Requirements

 * Python 3.11+
 * Ansible 2.16+
 * Panorama (this collection does NOT work for standalone firewalls or Strata Cloud Manager)
 * NGFWs connected to Panorama must be running Routed mode

### Install this collection

```shell
ansible-galaxy install paloaltonetworks.panos_policy_automation
```

### Define your Inventory

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

### Create your playbook and include the role

```yaml
---
- hosts: lab # <---- Replace this with your group 
  connection: local
  gather_facts: false
  name: Test the Lookup Policy playbook

  vars:
    provider:
      ip_address: "{{ ansible_host }}"
      username: "{{ lookup('env', 'ANSIBLE_NET_USERNAME') }}"
      password: "{{ lookup('env', 'ANSIBLE_NET_PASSWORD') }}"

  roles:
    - paloaltonetworks.panos_policy_automation.policy_creation # Note the included role

  tasks:
    - name: Print the results
      ansible.builtin.debug:
        msg: "{{ lookup_policy_security_policy_match_result }}"
```

### Execute the playbook

Note, replace the playbook and vars file names with your versions.

```shell
ansible-playbook your_playbook.yml -i inventory.yml --extra-vars=@vars_file.yml
```

## Need help?

Read the [docs](https://paloaltonetworks.github.io/ansible_panos_policy_orchestration/) for more information.

## Responsible AI Assistance Disclosure

Generative AI through the use of large language models has been used selectively in this repository
in the following ways:

1. Creating or editing documentation
