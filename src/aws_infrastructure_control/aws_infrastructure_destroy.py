import os
from from_root import from_root
from src.utils.common import read_config
import json

CONFIG_PATH = os.path.join(from_root(), 'src', 'aws_configurations', 'aws_config.yaml')
CONFIG_FILE = read_config(CONFIG_PATH)

INFRA_PATH = os.path.join(from_root(), 'src', 'aws_infrastructure')
os.chdir(INFRA_PATH)
SECRETS = os.environ.get("AWS_SECRETS")
SECRETS_JSON = json.loads(SECRETS)

os.system(f' terraform destroy '
          f'-var="access_key={SECRETS_JSON["aws_access_config"]["access_key"]}" '
          f'-var="secret_key={SECRETS_JSON["aws_access_config"]["secret_key"]}" '
          f'-var="region={CONFIG_FILE["aws_access_config"]["region"]}" '
          f'-var="bucket_name={CONFIG_FILE["aws_s3_bucket_config"]["s3_bucket_name"]}" '
          f'-var="sagemaker_role_name={CONFIG_FILE["aws_sagemaker_config"]["sagemaker_role_name"]}" '
          f'-var="allocated_storage={CONFIG_FILE["aws_database_config"]["allocated_storage"]}" '
          f'-var="engine={CONFIG_FILE["aws_database_config"]["engine"]}" '
          f'-var="engine_version={CONFIG_FILE["aws_database_config"]["engine_version"]}" '
          f'-var="mysql_db_name={CONFIG_FILE["aws_database_config"]["database_name"]}" '
          f'-var="mysql_username={CONFIG_FILE["aws_database_config"]["mysql_username"]}" '
          f'-var="mysql_password={CONFIG_FILE["aws_database_config"]["mysql_password"]}" '
          f'-var="instance_class={CONFIG_FILE["aws_database_config"]["instance_class"]}" '
          f'-var="parameter_group_name={CONFIG_FILE["aws_database_config"]["parameter_group_name"]}" '
          f'-var="skip_final_snapshot={CONFIG_FILE["aws_database_config"]["skip_final_snapshot"]}" '
          f'-var="security_group={CONFIG_FILE["aws_database_config"]["security_group_name"]}" '
          f'-var="vpc_id={CONFIG_FILE["aws_database_config"]["vpc_id"]}" '
          f'-var="identifier={CONFIG_FILE["aws_database_config"]["identifier"]}" '
          f'-var="publicly_accessible={CONFIG_FILE["aws_database_config"]["publicly_accessible"]}" '
          f'-var="sagemaker_policy_name={CONFIG_FILE["aws_sagemaker_config"]["sagemaker_policy_name"]}" '
          f'-var="ami={CONFIG_FILE["aws_ec2_instance_config"]["ami"]}" '
          f'-var="instance_type={CONFIG_FILE["aws_ec2_instance_config"]["instance_type"]}" '
          f'-var="availability_zone={CONFIG_FILE["aws_ec2_instance_config"]["availability_zone"]}" '
          f'-var="key_name={CONFIG_FILE["aws_ec2_instance_config"]["key_name"]}" ')
