from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud


async def validate_name_duplicate(name: str, session: AsyncSession) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        name, session
    )
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


def validate_project_not_closed(project) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )


def validate_full_amount_not_less_invested(
    new_full_amount: int, invested_amount: int
) -> None:
    if new_full_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                "Нельзя установить значение full_amount "
                "меньше уже вложенной суммы.",
            )
        )


def validate_project_has_no_investments(invested_amount: int) -> None:
    if invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )
