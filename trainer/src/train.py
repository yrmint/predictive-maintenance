import mlflow
from catboost import CatBoostClassifier


def train_model(x_train, y_train, features)\
        -> CatBoostClassifier:
    """
    Trains CatBoostClassifier. Tracks experiment using MLFlow.
    :param x_train: train dataset (features)
    :param y_train: train class labels
    :param features: list of features
    :return: trained classifier
    """

    mlflow.set_experiment("predictive-maintenance")

    with mlflow.start_run():
        mlflow.log_param("model_type", "CatBoostClassifier")
        mlflow.log_param("n_features", len(features))
        mlflow.log_param("train_samples", len(x_train))

        train_positive_rate = float(y_train.mean())
        mlflow.log_metric(
            "train_positive_rate",
            train_positive_rate,
        )

        cl = CatBoostClassifier(
            iterations=500,
            learning_rate=0.05,
            depth=6,
            loss_function="Logloss",
            eval_metric="AUC",
            random_seed=42,
            verbose=True,
            early_stopping_rounds=50
        )
        cl.fit(
            x_train, y_train
        )

    return cl
