from datetime import date, timedelta
import importlib
import pytest

import sys
sys.path.append('E:\\My\\PythonProjects\\photo_studios_aggregator_app')

from src.agregator.photostudios_parcer.photostudios import studios_list


@pytest.mark.asyncio
@pytest.mark.parametrize("photostudio", studios_list)
async def test_photostudios_positive(photostudio):
    studio = importlib.import_module(f"src.agregator.photostudios_parcer.photostudios.{photostudio}")
    assert await studio.get_schedule(date.today())
    assert await studio.get_schedule(date.today() + timedelta(days=10))

@pytest.mark.asyncio
@pytest.mark.parametrize("photostudio, yesterday", [(photostudio, date.today() - timedelta(days=1)) for photostudio in studios_list])
async def test_photostudios_negative(photostudio, yesterday):
    studio = importlib.import_module(f"src.agregator.photostudios_parcer.photostudios.{photostudio}")
    """with pytest.raises(ValueError):
        studio.get_schedule(yesterday)"""
    assert await studio.get_schedule(yesterday)
