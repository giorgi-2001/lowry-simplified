from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

from ..config import S3

from pathlib import Path
import os
import io
import uuid


media_path = Path(__file__).parent.parent.joinpath("media").joinpath("standards").resolve()

if not media_path.exists():
    media_path.mkdir(parents=True, exist_ok=True)


def extend_name(name: str):
    extentsion = str(uuid.uuid4())
    return name + "_" + extentsion


def process_data(content: bytes):
    data = io.StringIO(content.decode("utf-8"))
    df = pd.read_csv(data)

    df.columns = [col.lower() for col in df.columns]
    x_col_names = [col for col in df.columns if "x" in col or "c" in col]
    y_col_names = [col for col in df.columns if "y" in col or "e" in col]

    if not x_col_names or not y_col_names:
        raise ValueError("File is not formated correctly")
    
    x_col_name = x_col_names[0]

    df = df.dropna(subset=[x_col_name])

    x_col = df[x_col_name]
    y_cols = df[y_col_names]

    
    y_cols: pd.DataFrame = y_cols.apply(lambda row: row.fillna(row.mean()), axis=1)
    y_means = pd.Series(y_cols.mean(axis=1), name="y")

    concentration_uint = x_col_name.split("(")[1].replace(")", "")
    x_col.name = "x"

    # perform linear regression
    correlation = np.corrcoef(x_col, y_means)[0, 1]
    slope, y_intercept = np.polyfit(x_col, y_means, 1)
    regression = [x * slope + y_intercept for x in x_col]
    regr_serries = pd.Series(regression, name="regression")

    df = pd.concat([x_col, y_means, regr_serries], axis=1)

    return {
        "df": df,
        "info": {
            "unit": concentration_uint,
            "correlation": correlation,
            "slope": slope,
            "y_intercept": y_intercept
        }
    }


def plot_data_and_upload(data, name="plot"):
    x = data["df"]["x"]
    y = data["df"]["y"]
    regr = data["df"]["regression"]
    unit = data["info"]["unit"]

    plt.style.use("ggplot")

    plt.figure(figsize=(8, 6))
    plt.title(name.capitalize(), pad=20)
    plt.xlabel(f"Concentration ({unit})", labelpad=15)
    plt.ylabel("Extinsion", labelpad=15)

    plt.scatter(x, y, label="Standard Curve", color="blue")
    plt.plot(x, regr, label="Trendline", linewidth=2)

    plt.grid(visible=True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()

    plt.tight_layout()

    name = name.replace(" ", "_").strip()
    path = media_path / f"{name}.png"

    plt.savefig(path)
    plt.close()

    with open(path, "rb") as file:
        name = extend_name(name)
        content = file.read()
        file_url = S3.upload_image(content, f"standards/{name}.png")

    os.remove(path)

    return file_url



    