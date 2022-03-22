import yaml
import json
# from from_root import from_root
import os
import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def read_config(config_path):
    with open(config_path) as config_file:
        content = yaml.safe_load(config_file)

    return content


def read_json(path):
    json_file = open(path)
    content = json.load(json_file)
    json_file.close()

    return content


def update_config(config_path, data):
    with open(config_path, 'w') as config_file:
        config_file.write(yaml.dump(data, default_flow_style=False))
    return


def get_data():
    URL = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"

    try:
        df = pd.read_csv(URL, sep=";")
        return df
    except Exception as e:
        raise e


def evaluate(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == '__main__':
    path = os.path.join(os.getcwd(), 'aws_infrastructure/output.json')
    content = read_json(path)
    database_endpoint = content['values']['root_module']['resources'][0]['values']['address']
