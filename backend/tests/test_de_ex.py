import io
from pathlib import Path
import pytest
import pandas as pd
from src.experiments.DE import process_data, save_csv, plot_and_save


@pytest.fixture()
def patch_s3_upload(monkeypatch):
    def mock_upload_file(*args, **kwargs):
        return "s3-upload-url"
    monkeypatch.setattr(
        "src.experiments.DE.s3.upload_file",
        mock_upload_file
    )


@pytest.fixture
def standard_data():
    return {
        "slope": 0.5,
        "y_intercept": 0.355
    }


@pytest.fixture
def exp_content():
    file_path = Path(__file__).parent.joinpath("media").joinpath("data.csv")
    with open(file_path, "rb") as file:
        return file.read()


@pytest.fixture
def starting_df(exp_content):
    buffer = io.BytesIO(exp_content)
    return pd.read_csv(buffer)


@pytest.fixture
def final_dfs(exp_content, standard_data):
    return process_data(
        exp_content, standard_data["slope"], standard_data["y_intercept"]
    )


def test_process_data_success(starting_df, final_dfs):
    big_df, small_df = final_dfs
    assert big_df.shape[0] == starting_df.shape[0] + 2
    assert small_df.shape[0] == big_df.shape[1]
    assert "means" in small_df.columns
    assert "std" in small_df.columns


def test_save_csv_success(patch_s3_upload, starting_df):
    file_url = save_csv(starting_df)
    assert file_url == "s3-upload-url"


def test_plot_and_save_success(patch_s3_upload, final_dfs):
    small_df = final_dfs[1]
    file_url = plot_and_save(small_df, "Plot")
    assert file_url == "s3-upload-url"
