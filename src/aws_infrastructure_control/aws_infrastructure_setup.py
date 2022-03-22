import json
import os
from src.utils.common import read_config, read_json, update_config

CONFIG_PATH = os.path.join(os.getcwd(), 'src', 'aws_configurations', 'aws_config.yaml')
CONFIG_FILE = read_config(CONFIG_PATH)

INFRA_PATH = os.path.join(os.getcwd(), 'src', 'aws_infrastructure')
os.chdir(INFRA_PATH)

SECRETS = os.environ.get("AWS_SECRETS")
SECRETS_JSON = json.loads(SECRETS)

os.system(f' terraform plan '
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
          f'-var="key_name={CONFIG_FILE["aws_ec2_instance_config"]["key_name"]}"')

os.system(f' terraform apply '
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

os.system("terraform show -json > output.json")

os.system(f"mlflow sagemaker build-and-push-container --container {CONFIG_FILE['aws_ecr_config']['docker_image_name']}")

path = os.path.join(os.getcwd(), 'output.json')
content = read_json(path)

os.chdir("../../")

# mysql uri creation for mlflow server
database_endpoint = content['values']['root_module']['resources'][0]['values']['address']
database_name = CONFIG_FILE['aws_database_config']['database_name']
username = CONFIG_FILE['aws_database_config']['mysql_username']
password = CONFIG_FILE['aws_database_config']['mysql_password']

# update Config With aws mysql endpoint
aws_mysql_url = f"mysql://{username}:{password}@{database_endpoint}/{database_name}"

# Server command setup
server = f"mlflow server --backend-store-uri {aws_mysql_url} --artifacts-destination s3://{CONFIG_FILE['aws_s3_bucket_config']['s3_bucket_name']} --serve-artifacts --host 0.0.0.0 -p 8080"

# Tracking uri setup
public_dns = content['values']['root_module']['resources'][7]['values']['public_dns']
uri = f"http://{public_dns}:8080"

CONFIG_FILE['aws_database_config']['aws_mysql_url'] = database_endpoint
CONFIG_FILE['aws_server_config']['server_config'] = server
CONFIG_FILE['aws_server_config']['tracking_uri'] = uri

# Update Config
update_config(CONFIG_PATH, CONFIG_FILE)

