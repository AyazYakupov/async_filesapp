import pytest
from io import StringIO

from main import *
import asyncio
from files_app.models import File
from pytest_mock import mocker
import time

from files_app.routes import *
import setup
import config

Settings = config.CONFIG(test=True)


@pytest.yield_fixture
async def app(mocker):
    app = Sanic(__name__)
    from files_app.routes import bp
    app.blueprint(bp)

    yield app


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))


async def test_files_returns_200(test_cli):
    response = await test_cli.get('/')
    assert response.status == 200


async def test_files_put(test_cli):
    response = await test_cli.put('/')
    assert response.status == 405


async def test_files_post(test_cli):
    response = await test_cli.post('/', data={'file': StringIO('test content')})
    assert response.status == 200

    object_id = await db.fetch_one('select max(id) from files')

    with open(f'{Settings.get_files_dir()}{object_id[0]}_file') as f:
        assert f.read() == 'test content'
    os.remove(f'{Settings.get_files_dir()}{object_id[0]}_file')
    await db.execute(f'delete from files where id == {object_id[0]}')
