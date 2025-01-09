from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form
)

from .dao import StandardDao
from .shcemas import StandardData, StandardResponse
from ..tasks.standard_tasks import process_standard_data
from ..users.auth import user_dependency
from ..config import S3

from typing import Annotated, List


router = APIRouter(prefix="/standards", tags=["Standards"])


db_dependency = Annotated[StandardDao, Depends(StandardDao)]


@router.get("/")
async def list_all_standards(db: db_dependency) -> List[StandardResponse]:
    return await db.list_all_standards()


@router.post("/")
async def upload_file(
    user: user_dependency,
    name: str = Form(),
    description: str = Form(),
    file: UploadFile = File(),
) -> dict:
    content = await file.read()
    await file.close()
    result = process_standard_data.apply_async(
        args=(name, description, user.id, content)
    )
    return {"task_id": result.id}


@router.get("/my-standards")
async def get_standards_by_username(
    db: db_dependency,
    user: user_dependency
) -> List[StandardResponse]:
    return await db.get_standards_by_user_id(user.id)


@router.delete("/{id}")
async def delete_standard_by_id(
    id: int, db: db_dependency, user: user_dependency
) -> dict:
    standard = await db.get_standard_by_id(id)

    if not standard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Standard was not found"
        )
    
    if standard.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden Action"
        )
    
    file_name = "/".join(standard.image.split("/")[-2:])
    S3.delete_file(file_name)
    
    await db.delete_standrd_by_id(id)
    
    return {"detail": f"Standard {id} was deleted"}
