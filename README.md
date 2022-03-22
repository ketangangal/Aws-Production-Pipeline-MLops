# Aws-Production-Pipeline-MLops
An Automated production pipeline which includes aws infrastructure provisioning using terraform and CI-CD using git-hub actions.

# STEPS

## STEP 0 - CONFIG SETUP

* cd to src/aws_infrastructure and init terraform

```bash
terraform init
```
## STEP 1 - INFRA PROVISION

* run infra setup

```bash
python src/aws_infrastructure_control/aws_infrastructure_setup.py
```
### PLAN
### APPLY
### OUTPUT to JSON 
## STEP 2 - TRAINING
## STEP 3 - DEPLOY WITH RUNID
## STEP 4 - CONTROL AND MAINTAINENCE
## STEP - DESTROY

```bash
python src/aws_infrastructure_control/aws_infrastructure_setup.py
```

# Test Jenkin
