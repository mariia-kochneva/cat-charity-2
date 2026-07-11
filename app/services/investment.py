from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


def close_if_funded(obj, session):
    if obj.invested_amount >= obj.full_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now(timezone.utc)
        session.add(obj)


async def invest_funds(
    new_obj: CharityProject | Donation,
    session: AsyncSession,
):
    if isinstance(new_obj, Donation):
        db_objs = await charity_project_crud.get_open_projects(session)
    else:
        db_objs = await donation_crud.get_open_donations(session)

    for db_obj in db_objs:
        free_amount = new_obj.full_amount - new_obj.invested_amount
        if free_amount <= 0:
            break

        available_to_invest = db_obj.full_amount - db_obj.invested_amount
        investment = min(free_amount, available_to_invest)

        db_obj.invested_amount += investment
        new_obj.invested_amount += investment

        close_if_funded(db_obj, session)
        close_if_funded(new_obj, session)

    session.add(new_obj)
    for obj in db_objs:
        session.add(obj)

    await session.flush()
