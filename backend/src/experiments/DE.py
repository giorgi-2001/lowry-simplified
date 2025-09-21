import io
import uuid

import pandas as pd
from matplotlib import pyplot as plt

from ..aws import s3


def process_data(
    content: bytes, slope: float, y_intercept: float
):
    buffer = io.BytesIO(content)
    df = pd.read_csv(buffer)

    df.fillna(df.mean(), inplace=True)
    df = df.apply(lambda E: (E - y_intercept) / slope)

    means_df = df.mean().to_frame().T
    std_df = df.std().to_frame().T
    means_df.index = ["means"]
    std_df.index = ["std"]

    big_df = pd.concat([df, means_df, std_df])
    big_df = big_df.round(3)

    small_df = pd.concat([df.mean(), df.std()], axis=1)
    small_df.columns = ["means", "std"]

    return big_df, small_df


def save_csv(df: pd.DataFrame):
    file_name = f"csv/{uuid.uuid4().hex}.csv"
    with io.BytesIO() as buffer:
        df.to_csv(buffer)
        buffer.seek(0)
        content = buffer.read()
        return s3.upload_file(name=file_name, content=content)


def plot_and_save(df: pd.DataFrame, name: str, unit: str = "mg/ml"):
    x_values = [x for x in range(1, len(df.index) + 1)]
    plt.style.use("ggplot")

    plt.figure(figsize=(8, 6))
    plt.title(name.title(), pad=20)

    plt.xlabel("Groups", labelpad=15)
    plt.ylabel(f"Concentration ({unit})", labelpad=15)

    plt.xticks(
        ticks=x_values,
        labels=[str(i).capitalize() for i in df.index]
    )

    plt.bar(x=x_values, height=df["means"], yerr=df["std"], capsize=5)

    plt.grid(visible=True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    with io.BytesIO() as buf:
        file_name = f"experiments/{uuid.uuid4().hex}.png"
        plt.savefig(buf, format="png")
        buf.seek(0)
        content = buf.read()
        file_url = s3.upload_image(name=file_name, content=content)

    plt.close()
    return file_url
