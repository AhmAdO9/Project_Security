import os, sys
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.utils import save_object, load_object
from networksecurity.utils.utils import load_numpy_array_data, evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metrics import get_classification_score
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import(
            AdaBoostClassifier,
            GradientBoostingClassifier,
            RandomForestClassifier
)
from networksecurity.constants.training_pipeline import FINAL_MODEL_DIR
import mlflow, dagshub

# connecting to dagshub repository
dagshub.init(repo_owner='AhmAdO9', repo_name='Project_Security', mlflow=True)



class ModelTrainer:
    def __init__(self, 
                model_trainer_config:ModelTrainerConfig,         data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def track_mlflow(self, best_model, classification_metrics):
        with mlflow.start_run():
            f1_score = classification_metrics.f1_score
            precision_score = classification_metrics.precision_score
            recall_score = classification_metrics.recall_score

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)

            mlflow.sklearn.log_model(best_model, "model")


    def train_model(self, x_train, x_test, y_train, y_test):
        try:
            models = {
                "Random Forest":RandomForestClassifier(),
                "Decision Tree":DecisionTreeClassifier(),
                "Gradient Boosting":GradientBoostingClassifier(),
                "Logistic Regression":LogisticRegression(),
                "AdaBoost":AdaBoostClassifier()
            }

            params={

                "Random Forest":{
                    # 'criterion':['gini', 'entropy', 'log_loss'],
                    
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                },
                 "Decision Tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Gradient Boosting":{
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Logistic Regression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }
            
        }

            model_report:dict = evaluate_models(x_train = x_train, 
                                                x_test = x_test, 
                                                y_train = y_train, 
                                                y_test = y_test,
                                                models=models, params = params)

            best_model_name = sorted(model_report, key=lambda x : model_report[x]['score'], reverse=True)[0]

            best_estimator = model_report[best_model_name]['model']
            
            y_test_pred = best_estimator.predict(x_test)

            classification_test_metrics = get_classification_score(y_test, y_test_pred)

            ## Track the experiment with ML flow

            self.track_mlflow(best_estimator, classification_test_metrics)

            preprocessor_object =  load_object(file_path = self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            network_model = NetworkModel(preprocessor=preprocessor_object, model=best_estimator)
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=network_model)
            
            # final model

            save_object(file_path=f"{FINAL_MODEL_DIR}/model.pkl", obj=best_estimator)

            ## Model Trainer Artifact

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                # train_metric_artifact=None,
                                test_metrics_artifact=classification_test_metrics)

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, x_test, y_train, y_test = (
                train_arr[:, :-1],
                test_arr[:, :-1],
                train_arr[:, -1:],
                test_arr[:, -1:]
            ) 

            y_train = np.ravel(y_train)
            y_test = np.ravel(y_test)

            model_trainer_artifact = self.train_model(x_train, x_test, y_train, y_test)

            return model_trainer_artifact
            
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
