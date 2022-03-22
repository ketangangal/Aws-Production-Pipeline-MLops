from src.utils.sagemaker_utils import sagemaker_integration
from src.utils.common import read_config
from pathlib import Path
import argparse

if __name__ == "__main__":
    # Read config and sagemaker initialization
    config = read_config(Path("src/aws_configurations/aws_config.yaml"))
    sagemaker = sagemaker_integration(config)

    # Fetch Run id from command line as args
    args = argparse.ArgumentParser()
    args.add_argument("--runid", "-r", type=str, default=config['aws_endpoint_config']['run_id'])
    parsed_args = args.parse_args()

    # Switch Model
    response = sagemaker.switching_models(runid=parsed_args.runid)

    print(response)
