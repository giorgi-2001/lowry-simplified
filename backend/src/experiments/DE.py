import io

import pandas as pd

A = 0.0703
B = 0.45

df = pd.read_csv("data.csv")


def get_columns(content: bytes):
    data = io.BytesIO(content)
    df = pd.read_csv(data)
    return list(df.columns)


def process_data(
    df: pd.DataFrame, slope: float, y_intercept: float
):
    df = df.apply(lambda E: (E - y_intercept) / slope)
    df = pd.concat([df.mean(), df.std()], axis=1)
    df.columns = ["means", "std"]
    return df


print(df)
