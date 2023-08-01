import time
from typing import Any, Annotated

from fastapi import APIRouter, Depends, Form, UploadFile
from services.file import file_crud
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from auth.dto import UserDTO
from auth.services import get_current_active_user
from db.db import get_session
from dto.file_dto import FileDBDTO

router = APIRouter()


@router.get('/ping', responses={
    200: {'db': 'time'},
    500: {'db_status': 'down'}
})
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


@router.post('/files/upload')
async def upload_file(
        file: UploadFile,
        path: Annotated[str, Form()],
        current_user: Annotated[UserDTO, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_session)
) -> FileDBDTO | Any:
    return await file_crud.create_file(db=db,
                                       user=current_user,
                                       path=path,
                                       file=file)


@router.get('/files')
async def list_files(
        current_user: Annotated[UserDTO, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_session)
) -> list[FileDBDTO]:
    return await file_crud.get_multi(db=db, user=current_user)


@router.get('/files/download')
async def files_download(
        *,
        path: int | str,
        db: AsyncSession = Depends(get_session),
        current_user: Annotated[UserDTO, Depends(get_current_active_user)],
) -> Any:
    if isinstance(path, int):
        file_obj = await file_crud.get_by_fields(db=db,
                                                 user_id=current_user.id,
                                                 id=path)
        return file_obj.size
        # path = f'{user.id}/{obj.path}/{obj.name}'
    # return FileResponse(path=path, media_type="application/octet-stream")
