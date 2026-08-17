from catboost import CatBoostClassifier

def train_model(x_train, y_train) -> CatBoostClassifier:
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
