from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate
)
from app.services.investment import invest_funds, close_if_funded
from app.services.validators import (
    validate_name_duplicate,
    validate_project_not_closed,
    validate_full_amount_not_less_invested,
    validate_project_has_no_investments,
)


async def create_project(
    project_data: CharityProjectCreate,
    session: AsyncSession,
):
    await validate_name_duplicate(project_data.name, session)
    new_project = await charity_project_crud.create(project_data, session)
    await invest_funds(new_project, session)
    await session.commit()
    await session.refresh(new_project)
    return new_project


async def update_project(
    project: CharityProject,
    update_data: CharityProjectUpdate,
    session: AsyncSession,
):
    validate_project_not_closed(project)
    if update_data.full_amount is not None:
        validate_full_amount_not_less_invested(
            update_data.full_amount, project.invested_amount
        )
    if update_data.name is not None:
        await validate_name_duplicate(update_data.name, session)
    updated_project = await charity_project_crud.update(
        project, update_data, session
    )
    close_if_funded(updated_project, session)
    await session.commit()
    await session.refresh(updated_project)
    return updated_project


async def delete_project(
    project: CharityProject,
    session: AsyncSession,
):
    validate_project_has_no_investments(project.invested_amount)
    await charity_project_crud.remove(project, session)
    await session.commit()
    return project


async def get_all_projects(session: AsyncSession):
    return await charity_project_crud.get_multi(session)
