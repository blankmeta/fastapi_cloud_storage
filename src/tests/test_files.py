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
        with open(Path(self.FIXTURE_DIR, self.TEST_FILE_NAME), 'rb') as f:
            file_body = f.read()

        url = app.url_path_for('upload_file')
        response = await auth_ac.post(url, files={
            'file': file_body
        }, data={
            'path': self.TEST_REQUEST_FILE_PATH
        })

        assert response.status_code == status.HTTP_200_OK

    async def test_get_files(self, auth_ac: AsyncClient):
        url = app.url_path_for('list_files')
        response = await auth_ac.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
