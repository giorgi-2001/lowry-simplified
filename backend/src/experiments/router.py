import uuid
from fastapi import (
    APIRouter, Depends, HTTPException, status, UploadFile, File, Form
)
from .dao import ExperimentDAO
from .shcemas import ExpResponse
from ..users.auth import user_dependency
from ..standards.router import db_dependency as std_dependency
from ..projects.router import db_dependency as pj_dependency
from ..tasks.exp_tasks import build_experiment_files, remove_exp_files

from typing import Annotated, List


router = APIRouter(prefix="/experiments", tags=["Experiments"])


exp_dependency = Annotated[ExperimentDAO, Depends(ExperimentDAO)]


FORBIDEB_ERROR = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Forbiden action"
)


@router.get("/")
async def get_experiments_by_project_id(
    project_id: str, db: exp_dependency,
    user: user_dependency, pj: pj_dependency
) -> List[ExpResponse]:
    project = await pj.get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} does not exists"
        )
    if project.user_id != user.id:
        raise FORBIDEB_ERROR
    return await db.get_experiments_by_project_id(project_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_experiment(
    _: user_dependency,
    exp: exp_dependency,
    std: std_dependency,
    name: str = Form(..., min_length=2),
    description: str = Form(..., min_length=2),
    project_id: str = Form(...),
    standard_id: int = Form(...),
    file: UploadFile = File(),
):
    try:
        uuid.UUID(project_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

    valid_file_type = (
        file.filename.endswith(".csv") and file.content_type == "text/csv"
    )
    if not valid_file_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type"
        )

    standard = await std.get_standard_by_id(standard_id)
    if not standard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Standard {standard_id} does not exists"
        )
    experiment_data = {
        "name": name,
        "description": description,
        "project_id": project_id,
        "standard_id": standard_id
    }
    experiment_id = await exp.create_experiment(experiment_data)
    file_content = await file.read()

    # DE algorithm goes here:
    build_experiment_files.apply_async(kwargs={
        "experiment_id": experiment_id,
        "name": name,
        "content": file_content,
        "slope": standard.slope,
        "y_intercept": standard.y_intercept
    })

    return {"detail": f"Experiment {experiment_id} was created"}


@router.delete("/{experiment_id}")
async def delete_experiment(
    experiment_id: int, exp: exp_dependency, pj: pj_dependency,
    user: user_dependency
):
    experiment = await exp.get_experiments_by_id(experiment_id)
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experiment {experiment_id} does not exists"
        )

    project = await pj.get_project_by_id(experiment.project_id.hex)
    if project.user_id != user.id:
        raise FORBIDEB_ERROR

    remove_exp_files.apply_async(
        kwargs={"files": [experiment.image, experiment.csv]}
    )
    await exp.delete_experiment(experiment_id)
    return {"detail": f"Experiment {experiment_id} was deleted"}
