import asyncio
import pytest
from unittest.mock import MagicMock, patch
from src.tasks.standard_tasks import (
    _run_func_in_new_thread,
    async_to_sync,
)


async def async_add(x, y):
    await asyncio.sleep(0.01)
    return x + y


async def async_raise():
    await asyncio.sleep(0.01)
    raise ValueError("test error")


def test_run_func_in_new_thread_success():
    result = _run_func_in_new_thread(async_add, args=(2, 3), kwargs={})
    assert result == 5


def test_run_func_in_new_thread_with_kwargs():
    async def async_multiply(a, b=1):
        await asyncio.sleep(0.01)
        return a * b

    result = _run_func_in_new_thread(async_multiply, args=(4,), kwargs={"b": 5})
    assert result == 20


def test_run_func_in_new_thread_raises_error():
    with pytest.raises(ValueError) as exc:
        _run_func_in_new_thread(async_raise, args=(), kwargs={})
    assert str(exc.value) == "test error"


def test_async_to_sync_no_running_loop():
    """Test when there is no running event loop (uses run_until_complete)"""
    decorated = async_to_sync(async_add)
    result = decorated(2, 3)
    assert result == 5


def test_async_to_sync_running_loop(monkeypatch):
    """Test when an event loop is already running (calls _run_func_in_new_thread)"""

    # Fake running loop
    loop_mock = MagicMock()
    loop_mock.is_running.return_value = True

    # Patch asyncio.get_event_loop to return our mock loop
    monkeypatch.setattr("asyncio.get_event_loop", lambda: loop_mock)

    # Patch _run_func_in_new_thread to just return a fixed value
    with patch(
        "src.tasks.standard_tasks._run_func_in_new_thread",
        return_value=42
    ) as mock_thread:
        decorated = async_to_sync(async_add)
        result = decorated(1, 2)
        assert result == 42
        mock_thread.assert_called_once_with(async_add, (1, 2), {})


def test_async_to_sync_exception():
    """Test that exceptions in async function propagate"""
    decorated = async_to_sync(async_raise)
    with pytest.raises(ValueError) as exc:
        decorated()
    assert str(exc.value) == "test error"
