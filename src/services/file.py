import logging
from pathlib import Path

import aiofiles
from asyncpg import UniqueViolationError
from fastapi import UploadFile, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from dto.file_dto import FileDTO
from models.file import File
from .base import RepositoryDB


class RepositoryFile(RepositoryDB[File, FileDTO, FileDTO]):
    @staticmethod
    async def _save_file(user: User, path: str, content: bytes,
                         name: str) -> None:
        directory = f'{user.id}/{path}'
        path = Path(directory)
        if not Path.exists(path):
            Path(path).mkdir(parents=True, exist_ok=True)
        try:
            async with aiofiles.open(Path(path, name), 'wb') as buffer:
                await buffer.write(content)
        except UniqueViolationError as e:
            logging.warning(f'Error while file saving - {e}')
            raise HTTPException(status_code=409, detail='File already exists')

    async def create_file(self, db: AsyncSession, user: User, *,
                          file: UploadFile, path: str) -> Exception | File:
        content = file.file.read()
        size = len(content)
        name = file.filename
        db_obj = self._model(
            name=name,
            path=path,
            size=size,
            user_id=user.id
        )
        await self._save_file(user=user, path=path, content=content, name=name)
        try:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        except IntegrityError as e:
            logging.warning(f'Error file uploading - {e}')
            raise HTTPException(status_code=409, detail='File already exists')
        return db_obj


file_crud = RepositoryFile(File)
