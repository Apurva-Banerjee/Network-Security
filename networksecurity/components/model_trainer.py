import os
import sys
import mlflow
import mlflow.sklearn

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import load_object, save_object, load_numpy_array_data, evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_mlflow(self, best_model_name: str, best_model, train_metric, test_metric):
        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        mlflow.set_experiment("Network-Security-Phishing-Detection")

        with mlflow.start_run(run_name=best_model_name):
            mlflow.log_param("best_model", best_model_name)
            mlflow.log_params(best_model.get_params())

            mlflow.log_metric("train_f1_score", train_metric.f1_score)
            mlflow.log_metric("train_precision", train_metric.precision_score)
            mlflow.log_metric("train_recall", train_metric.recall_score)

            mlflow.log_metric("test_f1_score", test_metric.f1_score)
            mlflow.log_metric("test_precision", test_metric.precision_score)
            mlflow.log_metric("test_recall", test_metric.recall_score)

            mlflow.sklearn.log_model(sk_model=best_model, name="model")

    def train_model(self, X_train, y_train, X_test, y_test) -> ModelTrainerArtifact:
        models = {
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "KNN Classifier": KNeighborsClassifier(),
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(),
            "AdaBoost Classifier": AdaBoostClassifier(),
        }
        params = {
            "Decision Tree": {
                "criterion": ["gini", "entropy", "log_loss"],
                "splitter": ["best", "random"],
                "max_features": ["sqrt", "log2", None],
            },
            "Gradient Boosting": {
                "loss": ["log_loss", "exponential"],
                "learning_rate": [0.1, 0.01, 0.05, 0.001],
                "subsample": [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                "criterion": ["friedman_mse", "squared_error"],
                "max_features": ["sqrt", "log2", None],
            },
            "Random Forest": {
                "criterion": ["gini", "entropy", "log_loss"],
                "max_features": ["sqrt", "log2", None],
            },
            "KNN Classifier": {
                "n_neighbors": [3, 5, 7, 9],
                "weights": ["uniform", "distance"],
                "algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
            },
            "Logistic Regression": [
                {"solver": ["lbfgs", "newton-cg", "sag"], "C": [0.1, 1.0, 10.0, 100.0]},
                {"solver": ["liblinear"], "l1_ratio": [0, 1], "C": [0.1, 1.0, 10.0, 100.0]},
                {"solver": ["saga"], "l1_ratio": [0, 0.5, 1], "C": [0.1, 1.0, 10.0, 100.0]},
            ],
            "AdaBoost Classifier": {
                "n_estimators": [50, 100, 150],
                "learning_rate": [0.01, 0.1, 1.0],
            },
        }

        model_report: dict = evaluate_models(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            models=models,
            params=params,
        )

        # Get the best model score and name
        best_model_score = max(sorted(model_report.values()))
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model = models[best_model_name]

        y_train_pred = best_model.predict(X_train)
        classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)

        y_test_pred = best_model.predict(X_test)
        classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

        # Track the experiment with MLflow (single run with train + test metrics & params)
        self.track_mlflow(
            best_model_name=best_model_name,
            best_model=best_model,
            train_metric=classification_train_metric,
            test_metric=classification_test_metric,
        )

        # Load the actual preprocessor object and create model output directory
        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

        network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=network_model)

        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric,
        )
        logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
        return model_trainer_artifact

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact = self.train_model(X_train, y_train, X_test, y_test)
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)