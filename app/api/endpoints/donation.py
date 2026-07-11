from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.models.user import User
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB,
)
from app.services.donation import (
    create_donation, get_all_donations, get_donations_by_user
)


router = APIRouter(prefix="/donation", tags=["donations"])


@router.get(
    "/",
    response_model=list[DonationFullInfoDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations_endpoint(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_all_donations(session)


@router.post("/", response_model=DonationDB)
async def create_donation_endpoint(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await create_donation(donation, session, user)


@router.get(
    "/my",
    response_model=list[DonationDB],
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await get_donations_by_user(session, user)
