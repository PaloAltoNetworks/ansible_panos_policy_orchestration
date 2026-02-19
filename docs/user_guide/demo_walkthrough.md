# Red Hat/PAN Joint Demo Notes and Walkthrough

## Lab Environment

**Devices** 
1xPanorama (Azure)
1xVM-Series (Azure)

**Working, connected Zones**
Trust (Working)
Untrust (Working)

**Example Only Zones**
Web
Database
CCTV 

## Run

Example Web to DB

Run the lookup first
```shell
ansible-playbook -i inventory_real.yml --extra-vars=@./example_vars_file_web_to_db.yml paloaltonetworks.panos_policy_automation.examples.lookup_policy
```

Then, run creation

```shell
ansible-playbook -i inventory_real.yml --extra-vars=@./example_vars_file_web_to_db.yml paloaltonetworks.panos_policy_automation.examples.create_policy
```
