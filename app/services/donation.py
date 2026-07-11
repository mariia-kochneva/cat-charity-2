from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate
from app.services.investment import invest_funds


async def create_donation(
    donation_data: DonationCreate,
    session: AsyncSession,
    user: User,
):
    new_donation = await donation_crud.create(donation_data, session, user)
    await invest_funds(new_donation, session)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


async def get_all_donations(session: AsyncSession):
    return await donation_crud.get_multi(session)


async def get_donations_by_user(session: AsyncSession, user: User):
    return await donation_crud.get_by_user(session, user)
