from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.charity_project import (
    create_project,
    update_project,
    delete_project,
    get_all_projects,
)
from app.services.utils import get_project_or_404


router = APIRouter(prefix="/charity_project", tags=["charity_projects"])


@router.get("/", response_model=list[CharityProjectDB])
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_all_projects(session)


@router.post(
    "/",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await create_project(project, session)


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await get_project_or_404(project_id, session)
    return await update_project(project, obj_in, session)


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await get_project_or_404(project_id, session)
    return await delete_project(project, session)
