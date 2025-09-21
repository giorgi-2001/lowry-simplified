from celery import Task
from ..celery_worker import celery_worker
from ..experiments.DE import process_data, save_csv, plot_and_save
from ..experiments.dao import ExperimentDAO
from .standard_tasks import async_to_sync


@async_to_sync
async def save_csv_and_img(
    experiment_id: int, csv_url: str, img_url: str, dao=ExperimentDAO
):
    await dao.update_file(experiment_id, csv_url, "csv")
    await dao.update_file(experiment_id, img_url, "img")


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


build_experiment_files: Task
