# Ansible PAN-OS Policy Automation

![GitHub commit activity](https://img.shields.io/github/commit-activity/w/adambaumeister/ansible_panos_policy_orchestration)
![GitHub commits difference between two branches/tags/commits](https://img.shields.io/github/commits-difference/adambaumeister/ansible_panos_policy_orchestration?base=master&head=develop&label=Changes%20Pending%20Release)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/adambaumeister/ansible_panos_policy_orchestration/ci.yml)
![GitHub License](https://img.shields.io/github/license/adambaumeister/ansible_panos_policy_orchestration)
![GitHub Repo stars](https://img.shields.io/github/stars/adambaumeister/ansible_panos_policy_orchestration)
![GitHub Release](https://img.shields.io/github/v/release/adambaumeister/ansible_panos_policy_orchestration)
![Github Pages](https://img.shields.io/badge/github-pages-black?logo=githubpages&link=https%3A%2F%2Fadambaumeister.github.io%2Fansible_panos_policy_orchestration%2F)

Docs: https://adambaumeister.github.io/ansible_panos_policy_orchestration/

This repository provides a framework and a philosophy for creating PAN-OS security policies
via Automation.

This repository would be of interest to you if:

 * You deal with a large number of incoming user requests for security policy
 * You can make repeatable, actionable policy decisions 
 * You are comfortable with Ansible or General automation platforms.

## Quickstart

### Requirements

 * 🐍 Python 3.11+
 * Ansible 2.16+


### Install the Paloaltonetworks Collection

```shell
ansible-galaxy install paloaltonetworks.panos
```

### Clone this repo

```shell
# ssh
git clone git@github.com:adambaumeister/ansible_panos_policy_orchestration.git
# https
https://github.com/adambaumeister/ansible_panos_policy_orchestration.git
```

### Define your Inventory

```yaml title='inventory.yml'
all:
  children:
    # the `lab` group is included here as an example, but you can layout your panorama devices however you like.
    # Note you will need to create your own primary playbook mirroring `lab_policy.yml` if you change the grouping.
    lab:
      hosts:
        lab-panorama01:
          ansible_host: < YOUR PANORAMA HOSTNAME OR IP HERE >
          # Password should be provided via PAN_PASSWORD environment variable
          # Example: export PAN_PASSWORD="admin_password"
          
          # Username should be provided via PAN_USERNAME environment variable
          # Example: export PAN_USERNAME="admin"
      vars:
        # Common variables for lab environment
        ansible_connection: local
        ansible_python_interpreter: "{{ ansible_playbook_python }}"
        # These variables are only used when creating COMPLETELY NEW policies
        default_new_policy_device_group: Lab
        default_new_policy_rulebase: post-rulebase
        default_new_policy_tag: AUTOMATED
        default_rule_location: bottom
```

### Run the connectivity playbook to validate connectivity

```shell
ansible-playbook playbooks/testing/connectivity.yml
```
