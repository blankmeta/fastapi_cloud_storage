import logging
from pathlib import Path
from typing import Optional, Any

import aiofiles
from asyncpg import UniqueViolationError
from fastapi import UploadFile, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from core.config import FILES_FOLDER
from dto.file_dto import FileDTO
from models.file import File
from .base import RepositoryDB, ModelType


class RepositoryFile(RepositoryDB[File, FileDTO, FileDTO]):
    async def get_by_fields(
            self,
            db: AsyncSession,
            **kwargs
    ) -> Optional[ModelType]:
        conditions = [getattr(self._model, key) == value for key, value in
                      kwargs.items()]
        statement = select(
            self._model
        ).where(
            and_(*conditions)
        )
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def get_by_id(
            self,
            db: AsyncSession,
            user: User,
            id: Any
    ) -> Optional[ModelType]:
        statement = select(
            self._model
        ).where(
            self._model.id == id,
            self._model.user_id == user.id)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    @staticmethod
    async def _save_file(user: User, path: str, content: bytes,
                         name: str) -> None:
        directory = f'{user.id}/{path}'
        path = Path(FILES_FOLDER, directory)
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
        file_content = file.file.read()
        db_obj = self._model(
            name=file.filename,
            path=path,
            size=len(file_content),
            user_id=user.id
        )
        await self._save_file(user=user, path=path, content=file_content,
                              name=file.filename)
        try:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        except IntegrityError as e:
            logging.warning(f'Error file uploading - {e}')
            raise HTTPException(status_code=409, detail='File already exists')
        return db_obj


file_crud = RepositoryFile(File)
