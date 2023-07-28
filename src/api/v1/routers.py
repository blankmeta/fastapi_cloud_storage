from typing import Any, Annotated

from fastapi import APIRouter, Depends, Form, UploadFile, HTTPException
from services.file import file_crud
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dto import UserDTO
from auth.services import get_current_active_user
from db.db import get_session
from dto.file_dto import FileDBDTO

router = APIRouter()


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

# TODO: files downloading
