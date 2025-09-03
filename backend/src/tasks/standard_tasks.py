from ..celery_worker import celery_worker
from ..standards.DE import process_data, plot_data_and_upload
from ..standards.dao import StandardDao
from concurrent.futures import ThreadPoolExecutor
import asyncio
import functools

from celery import Task


def _run_func_in_new_thread(func, args, kwargs):
    with ThreadPoolExecutor() as executor:
        result = executor.submit(asyncio.run(func(*args, **kwargs)))
        return result.result()


def async_to_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()

        if not loop.is_running():
            result = loop.run_until_complete(func(*args, **kwargs))
        else:
            _run_func_in_new_thread(func, args, kwargs)
        return result
    return wrapper


@async_to_sync
async def save_standard_to_db(data):
    return await StandardDao.create_standard(data)


@celery_worker.task
def process_standard_data(
    name: str, description: str, user_id: int, content: bytes
):
    data = process_data(content)
    file_url = plot_data_and_upload(data, name)

    standard_data = {
        "name": name,
        "description": description,
        "image": file_url,
        "correlation": data["info"]["correlation"],
        "slope": data["info"]["slope"],
        "y_intercept": data["info"]["y_intercept"],
        "user_id": user_id
    }

    return save_standard_to_db(standard_data)


process_standard_data: Task
