from fastapi import APIRouter, Depends, HTTPException, status

from .dao import ProjectDAO
from .shcemas import ProjectData, ProjectResponse
from ..users.auth import user_dependency

from typing import Annotated, List


router = APIRouter(prefix="/projects", tags=["Projects"])


db_dependency = Annotated[ProjectDAO, Depends(ProjectDAO)]


NOT_FOUND_ERROR = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Project was not found"
)

FORBIDEB_ERROR = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Forbiden action"
)


@router.get("/")
async def get_projects(
    user: user_dependency, db: db_dependency
) -> List[ProjectResponse]:
    return await db.list_all_projects(user_id=user.id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectData,
    user: user_dependency,
    db: db_dependency,
) -> dict:
    project_data_dict = project_data.model_dump()
    project_data_dict.update({"user_id": user.id})
    project_id = await db.create_project(project_data=project_data_dict)
    return {"detail": f"Project {project_id} was created"}


@router.get("/{project_id}")
async def get_project_by_id(
    project_id: str, db: db_dependency, user: user_dependency
) -> ProjectResponse:
    project = await db.get_project_by_id(project_id)

    if not project:
        raise NOT_FOUND_ERROR

    if project.user_id != user.id:
        raise FORBIDEB_ERROR

    return project


@router.put("/{project_id}")
async def update_project(
    project_id: str,
    project_data: ProjectData,
    db: db_dependency,
    user: user_dependency
) -> dict:
    project = await db.get_project_by_id(project_id)
    if not project:
        raise NOT_FOUND_ERROR

    if project.user_id != user.id:
        raise FORBIDEB_ERROR

    project = await db.update_project(
        project_id=project_id, project_data=project_data.model_dump()
    )

    return {"detail": f"Project {project} was deleted"}


@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    db: db_dependency,
    user: user_dependency
):
    project = await db.get_project_by_id(project_id)
    if not project:
        raise NOT_FOUND_ERROR

    if project.user_id != user.id:
        raise FORBIDEB_ERROR
    exp_ids = await db.get_experiment_ids(project_id)

    if exp_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There are still experiments assosiated with this project. Make sure to remove them first."
        )

    project = await db.delete_project(project_id)
    return {"detail": f"Project {project} was deleted"}
