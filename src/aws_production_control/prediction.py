from src.utils.sagemaker_utils import sagemaker_integration
from src.utils.common import read_config
from pathlib import Path
import pandas as pd


data = pd.read_json('{"fixed acidity":{"0":7.4},"volatile acidity":{"0":0.7},"citric acid":{"0":0},"residual sugar":{'
                    '"0":1.9},"chlorides":{"0":0.076},"free sulfur dioxide":{"0":11},"total sulfur dioxide":{"0":34},'
                    '"density":{"0":0.9978},"pH":{"0":3.51},"sulphates":{"0":0.56},"alcohol":{"0":9.4}}')

if __name__ == "__main__":
    # Read config and sagemaker initialization
    config = read_config(Path("src/aws_configurations/aws_config.yaml"))
    sagemaker = sagemaker_integration(config)

    # Json query and response
    input_json = data.to_json(orient='split')
    Response = sagemaker.query(input_json)
    print(f"Predictions From Model EndPoint : {Response}")

