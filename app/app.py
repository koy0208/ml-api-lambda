import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
from boto3 import Session
from typing import List

app = FastAPI()

class Features(BaseModel):
    RM:float
    AGE:float

@app.get("/health")
async def get_health():
    return {"message": "OK"}

@app.post("/predict")
async def post_predict(features:List[Features]):
    # S3からモデル読み込み
    session = Session()
    s3client = session.client("s3")
    model_obj = s3client.get_object(Bucket="my-boston-model", Key="boston.model")
    model = pickle.loads(model_obj["Body"].read())
    # PUTされたjsonをpndasに整形
    rm_list = [feature.RM for feature in features]
    age_list = [feature.AGE for feature in features]
    df_feature = pd.DataFrame({
        "RM" :rm_list,
        "AGE":age_list
    })
    # 予測結果をjsonに変換
    pred = model.predict(df_feature)
    responce = [{"predict":p} for p in pred]
    return responce

handler = Mangum(app)