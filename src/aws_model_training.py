import os
import argparse
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
from src.utils.common import get_data, evaluate, read_config
import mlflow
import mlflow.sklearn

def main(alpha, l1_ratio, tracking_uri):
    df = get_data()

    train, test = train_test_split(df)

    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)

    train_y = train[["quality"]]
    test_y = test[["quality"]]

    # mlflow tracking URI
    mlflow.set_tracking_uri(tracking_uri)

    with mlflow.start_run():
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42, max_iter=1000)
        lr.fit(train_x, train_y)

        pred = lr.predict(test_x)
        rmse, mae, r2 = evaluate(test_y, pred)

        print(f"Elastic net params: alpha: {alpha}, l1_ratio: {l1_ratio}")
        print(f"Elastic net metric: rmse:{rmse}, mae: {mae}, r2:{r2}")

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_param("max_iter", 1000)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(lr, "model", registered_model_name="ElasticnetWineModel")
        else:
            mlflow.sklearn.log_model(lr, "model")


if __name__ == "__main__":
    CONFIG_FILE = read_config(config_path='./src/aws_configurations/aws_config.yaml')
    print(CONFIG_FILE['aws_server_config']['tracking_uri'])
    args = argparse.ArgumentParser()
    args.add_argument("--alpha", "-a", type=float, default=0.5)
    args.add_argument("--l1_ratio", "-l1", type=float, default=0.5)
    args.add_argument("--tracking_uri", "-t", type=str, default=CONFIG_FILE['aws_server_config']['tracking_uri'])
    parsed_args = args.parse_args()
    try:
        main(alpha=parsed_args.alpha, l1_ratio=parsed_args.l1_ratio,
             tracking_uri=parsed_args.tracking_uri)

    except Exception as e:
        raise e


