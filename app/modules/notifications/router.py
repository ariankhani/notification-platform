from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.core.deps import CurrentUserDep, SessionDep

from . import services
from .schemas import (
    NotificationCreate,
    NotificationResponse,
    NotificationRuleCreate,
    NotificationRuleResponse,
    NotificationRuleUpdate,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])



@router.get("/my", response_model=list[NotificationResponse])
async def get_my_notifications(
    current_user: CurrentUserDep,
    session: SessionDep,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, le=100),
):
    return await services.get_user_notifications(
        session=session,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )


@router.post("/rules", response_model=NotificationRuleResponse, status_code=201)
async def create_rule(
    data: NotificationRuleCreate,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    try:
        return await services.create_notification_rule(session, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/rules", response_model=list[NotificationRuleResponse])
async def list_rules(
    current_user: CurrentUserDep,
    session: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    event_type: Annotated[str | None, Query(description="فیلتر بر اساس نوع رویداد")] = None,
):
    return await services.list_notification_rules(
        session, skip=skip, limit=limit, event_type=event_type
    )


@router.patch("/rules/{rule_id}", response_model=NotificationRuleResponse)
async def update_rule(
    rule_id: int,
    data: NotificationRuleUpdate,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    try:
        return await services.update_notification_rule(session, rule_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/rules/{rule_id}", status_code=204)
async def delete_rule(
    rule_id: int,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    try:
        deleted = await services.delete_notification_rule(session, rule_id)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if not deleted:
        raise HTTPException(status_code=404, detail="Rule not found")



@router.post("/", response_model=NotificationResponse, status_code=201)
async def create_notification(
    data: NotificationCreate,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    if data.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create notifications for another user",
        )
    try:
        return await services.create_notification(session, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
