import os
import pandas as pd
import sys
from source.exceptions import CustomException
from source.logger import logging
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from source.components.data_transformation import DataTransformation
from source.components.data_transformation import DataTransformationConfig
from source.components.model_training import ModelTrainer
from source.components.model_training import ModelTrainerConfig

@dataclass
class DataIngestionConfig:
    train_data_path: str = None
    test_data_path: str = None
    raw_data_path: str = None
    
    def __post_init__(self):
        if self.train_data_path is None:
            self.train_data_path = os.path.join("artifacts", "train.csv")
        if self.test_data_path is None:
            self.test_data_path = os.path.join("artifacts", "test.csv")
        if self.raw_data_path is None:
            self.raw_data_path = os.path.join("artifacts", "data.csv")
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config= DataIngestionConfig()
        
    def initiate_data_ingestion(self):
        logging.info("Entered data ingestion method or component")
        
        try:
            df=pd.read_csv("notebook\data\stud.csv")
            logging.info("Raed dataset as dataframe") 
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            logging.info("Train Test Split inintiated")
            
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info("Ingestion of data is complete")
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )       
       
        
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data, test_data= obj.initiate_data_ingestion()
    
    data_transformation = DataTransformation()
    train_arr, test_arr = data_transformation.initiate_data_transformation(train_data, test_data)
    
    model_trainer = ModelTrainer()
    result = model_trainer.initiate_model_trainer(train_arr, test_arr)
    print(result)