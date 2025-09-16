from pathlib import Path
from unittest.mock import patch, mock_open

import pytest
import numpy as np
import pandas as pd

from src.standards.DE import (
    extend_name, process_data, plot_data_and_upload
) 


@pytest.fixture
def fixed_uuid(monkeypatch):
    mock_id = "c1f20fafbbfb4885bc619227c9e87554"
    monkeypatch.setattr(
        "src.standards.DE.uuid.uuid4",
        lambda: mock_id
    )
    return mock_id


@pytest.fixture
def valid_csv_content():
    csv_file_path = (
        Path(__file__).parent.joinpath("media")
        .joinpath("standard.csv").resolve()
    )
    with open(csv_file_path, "rb") as content:
        return content.read()
    

@pytest.fixture
def means_data():
    return [
        0.083333, 0.210000, 0.303333, 0.396667,
        0.486667, 0.580000, 0.666667, 0.760000,
        0.846667, 0.943333
    ]


@pytest.fixture
def regression_data():
    return [
        0.115598, 0.206162, 0.296727, 0.387291,
        0.477856, 0.568421, 0.658985, 0.749550,
        0.840115, 0.975962
    ]


@pytest.fixture
def sample_data():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({
        "x": [1, 2, 3],
        "y": [2, 4, 6],
        "regression": [2.0, 4.0, 6.0]
    })
    return {
        "df": df,
        "info": {"unit": "mg"}
    }


def test_extend_name(fixed_uuid):
    name_to_extend = "elisa"
    extended_name = extend_name(name_to_extend)
    assert extended_name == f"{name_to_extend}_{fixed_uuid}"


def test_process_data_happy_path(
        valid_csv_content, means_data, regression_data
    ):
    result = process_data(valid_csv_content)

    df = result["df"]
    info = result["info"]

    # ---- dataframe checks ----
    assert list(df.columns) == ["x", "y", "regression"]
    assert not df["x"].isna().any()

    # row means: (2+3)/2 = 2.5; (4)/1 =4; (6)/1 =6
    expected_y = pd.Series(means_data, name="y")
    pd.testing.assert_series_equal(df["y"], expected_y)

    # row regression
    expected_regr = pd.Series(regression_data, name="regression")
    pd.testing.assert_series_equal(df["regression"], expected_regr)

    # ---- info checks ----
    assert info["unit"] == "mg/ml"
    assert pytest.approx(info["slope"], rel=1e-6) == np.polyfit(df["x"], df["y"], 1)[0]
    assert -1 <= info["correlation"] <= 1


def test_process_data_missing_x_or_y():
    bad_csv = b"a,b,c\n1,2,3\n"
    with pytest.raises(ValueError, match="File is not formated correctly"):
        process_data(bad_csv)


def test_process_data_drops_rows_with_na_x():
    csv_file_path = (
        Path(__file__).parent.joinpath("media")
        .joinpath("invalid.csv").resolve()
    )

    with open(csv_file_path, "rb") as file:
        content = file.read()

    result = process_data(content)

    df = result["df"]
    assert df.shape[0] == 7
    for val in df["y"]:
        assert not pd.isna(val)
    for val in df["regression"]:
        assert not pd.isna(val)


def test_process_data_case_insensitive_columns():
    content = b"""x (mg),Y
1,10
"""
    result = process_data(content)
    df = result["df"]
    assert set(df.columns) == {"x", "y", "regression"}
    assert df["x"].iloc[0] == 1.0
    assert df["y"].iloc[0] == 10.0


def test_regression_line_matches_points():
    # Perfect line: y = 2*x + 1
    content = b"""X (mg),Y
1,3
2,5
3,7
"""
    res = process_data(content)
    slope = res["info"]["slope"]
    intercept = res["info"]["y_intercept"]
    x = res["df"]["x"]
    y = res["df"]["y"]
    predicted = slope * x + intercept
    assert np.allclose(predicted, y, rtol=1e-8)
    # Slope should be ~2, intercept ~1
    assert pytest.approx(2.0, rel=1e-8) == slope
    assert pytest.approx(1.0, rel=1e-8) == intercept


def test_all_y_nan_in_row():
    content = b"""X (mg),Y1,Y2
1,,
"""
    res = process_data(content)
    # y mean should stay NaN since no non-NaN values in that row
    assert res["df"]["y"].isna().iloc[0]


def test_plot_data_and_upload(sample_data):
    fake_url = "https://s3.fakeurl.com/standards/plot.png"

    with patch("src.standards.DE.plt.savefig") as mock_savefig, \
         patch("src.standards.DE.plt.close") as mock_close, \
         patch("builtins.open", mock_open(read_data=b"fakecontent")) as mock_file, \
         patch("src.standards.DE.S3.upload_image", return_value=fake_url) as mock_upload, \
         patch("src.standards.DE.extend_name", side_effect=lambda name: name + "_123"), \
         patch("os.remove") as mock_remove:

        result_url = plot_data_and_upload(sample_data, name="plot")

    # ---- assertions ----
    mock_savefig.assert_called_once()   # figure was saved
    mock_close.assert_called_once()     # figure was closed
    mock_file.assert_called_once()      # file was opened
    mock_upload.assert_called_once()    # S3 upload called
    mock_remove.assert_called_once()    # file removed

    # Check returned URL
    assert result_url == fake_url