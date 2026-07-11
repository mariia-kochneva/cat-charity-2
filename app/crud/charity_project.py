from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        name: str,
        session: AsyncSession,
    ):
        result = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == name
            )
        )
        return result.scalars().first()

    async def get_open_projects(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == False  # noqa
            ).order_by(CharityProject.create_date)
        )
        return projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
