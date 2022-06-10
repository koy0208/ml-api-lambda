import pandas as pd
import pickle
import boto3
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def main():
    boston = load_boston()

    X  = pd.DataFrame(boston.data, columns=boston.feature_names)
    # 部屋の広さと築年数を使う
    X = X[["RM", "AGE"]]
    y = boston.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

    mod = LinearRegression()
    mod.fit(X_train, y_train)

    # モデルの保存
    with open("boston.model", "wb") as f:
        pickle.dump(mod, f)

    # バケット作成
    BUCKET_NAME = "my-boston-model"

    session = boto3.Session()
    s3_client = session.client("s3")
    location={'LocationConstraint': 'ap-northeast-1'}
    # バケットがすでにあればエラーになる。
    try:
        s3_client.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration=location)
    except:
        pass

    # S3にアップロード
    s3_client.upload_file("boston.model", BUCKET_NAME, "boston.model")

if __name__ == "__main__": 
    main() 

