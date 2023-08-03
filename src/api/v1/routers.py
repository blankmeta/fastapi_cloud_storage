import time
from pathlib import Path
from typing import Any, Annotated

from fastapi import APIRouter, Depends, Form, UploadFile, HTTPException
from fastapi.responses import FileResponse
from starlette import status

from services.file import file_crud
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from auth.dto import UserRequestDTO, UserDTO
from auth.services import get_current_active_user
from core.config import FILES_FOLDER
from db.db import get_session
from dto.file_dto import FileDBDTO

router = APIRouter()


@router.get('/ping',
            responses={
                status.HTTP_200_OK: {'db': 'time'},
                status.HTTP_500_INTERNAL_SERVER_ERROR: {'db_status': 'down'}
            },
            summary='Доступность базы данных',
            description='Точка для пинга базы данных в секундах')
async def ping_db(
        db: AsyncSession = Depends(get_session)
) -> Any:
    try:
        start = time.time()
        statement = select(1)
        await db.execute(statement)
        return JSONResponse(status_code=200, content={
            'db': time.time() - start
        })
    except ConnectionRefusedError:
        return JSONResponse(status_code=500, content={
            'db_status': 'down',
        })


@router.post('/files/upload',
             summary='Загрузка файла в хранилище.',
             description='Точка для загрузки файла любого типа в облако.')
async def upload_file(
        file: UploadFile,
        path: Annotated[str, Form()],
        current_user: Annotated[
            UserRequestDTO, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_session)
) -> FileDBDTO | Any:
    return await file_crud.create_file(db=db,
                                       user=current_user,
                                       path=path,
                                       file=file)


@router.get('/files',
            summary='Получение всех файлов.',
            description='Точка для получения списка всех файлов пользователя.')
async def list_files(
        current_user: Annotated[
            UserRequestDTO, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_session)
) -> list[FileDBDTO]:
    return await file_crud.get_multi(db=db, user=current_user)


@router.get('/files/download',
            summary='Загрузка файлов.',
            description='Точка для скачивания файла по его id или пути.')
async def files_download(
        *,
        path: int | str,
        db: AsyncSession = Depends(get_session),
        current_user: Annotated[UserDTO, Depends(get_current_active_user)],
) -> FileResponse:
    if isinstance(path, int):
        file_obj = await file_crud.get_by_fields(db=db,
                                                 user_id=current_user.id,
                                                 id=path)
    else:
        file_path = '/'.join(path.split('/')[:-1])
        file_name = path.split('/')[-1]
        file_obj = await file_crud.get_by_fields(db=db,
                                                 user_id=current_user.id,
                                                 path=file_path,
                                                 name=file_name)
    if not file_obj:
        raise HTTPException(status_code=404, detail='Not found')
    file_folder = Path(FILES_FOLDER, str(current_user.id), file_obj.path,
                       file_obj.name)
    return FileResponse(path=file_folder,
                        media_type="application/octet-stream")
