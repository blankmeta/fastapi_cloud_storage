import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from starlette import status

from core.config import FILES_FOLDER
from main import app

client = TestClient(app)


class TestFiles:
    FIXTURE_DIR = Path(Path(__file__).parent.resolve(), 'fixtures')
    TEST_FILE_NAME = 'imgtest.png'
    TEST_REQUEST_FILE_PATH = 'some_path'

    async def test_file_upload(self, auth_ac: AsyncClient):
        url = app.url_path_for('upload_file')
        response = await auth_ac.post(url, files={
            'file': open(Path(self.FIXTURE_DIR, self.TEST_FILE_NAME), 'rb')
        }, data={
            'path': self.TEST_REQUEST_FILE_PATH
        })

        assert response.status_code == status.HTTP_200_OK

    async def test_existing_file_upload(self, auth_ac: AsyncClient):
        url = app.url_path_for('upload_file')
        response = await auth_ac.post(url, files={
            'file': open(Path(self.FIXTURE_DIR, self.TEST_FILE_NAME), 'rb')
        }, data={
            'path': self.TEST_REQUEST_FILE_PATH
        })

        assert response.status_code == status.HTTP_409_CONFLICT

    async def test_get_files(self, auth_ac: AsyncClient):
        url = app.url_path_for('list_files')
        response = await auth_ac.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    async def test_download_file_by_id(self, auth_ac: AsyncClient):
        url = app.url_path_for('files_download')
        response = await auth_ac.get(url, params={
            'path': 1
        })

        assert response.status_code == status.HTTP_200_OK

    async def test_download_file_by_path(self, auth_ac: AsyncClient):
        url = app.url_path_for('files_download')
        response = await auth_ac.get(url, params={
            'path': f'{self.TEST_REQUEST_FILE_PATH}/{self.TEST_FILE_NAME}'
        })

        assert response.status_code == status.HTTP_200_OK

    async def test_download_unexisting_file(self, auth_ac: AsyncClient):
        url = app.url_path_for('files_download')
        response = await auth_ac.get(url, params={
            'path': f'{self.TEST_REQUEST_FILE_PATH}/something.png'
        })

        assert response.status_code == status.HTTP_404_NOT_FOUND
