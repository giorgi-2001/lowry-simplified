from typing import List
from celery import Task
from ..celery_worker import celery_worker
from ..experiments.DE import process_data, save_csv, plot_and_save
from ..experiments.dao import ExperimentDAO
from ..aws import s3
from .standard_tasks import async_to_sync


@async_to_sync
async def save_csv_and_img(
    experiment_id: int, csv_url: str, img_url: str, dao=ExperimentDAO
):
    await dao.update_file(experiment_id, csv_url, "csv")
    await dao.update_file(experiment_id, img_url, "img")


@async_to_sync
async def get_experiment(exp_id: int, dao=ExperimentDAO):
    return await dao.get_experiments_by_id(exp_id)


def get_files(experiment_id: int):
    exp = get_experiment(experiment_id)
    print("Experiment: ", exp)
    if exp:
        img = "/".join(exp.image.split("/")[-2:])
        csv = "/".join(exp.csv.split("/")[-2:])
        return img, csv


@celery_worker.task
def build_experiment_files(
    experiment_id: int,
    content: bytes,
    name: str,
    slope: float,
    y_intercept: float
):
    big_df, small_df = process_data(content, slope, y_intercept)
    csv_url = save_csv(big_df)
    img_url = plot_and_save(small_df, name)
    save_csv_and_img(experiment_id, csv_url, img_url)


@celery_worker.task
def remove_exp_files(*, files: List[str]):
    for file in files:
        file_name = "/".join(file.split("/")[-2:])
        s3.delete_file(file_name)


build_experiment_files: Task
remove_exp_files: Task
