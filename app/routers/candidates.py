from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session
from starlette import status

from app import models
from app.database import get_db
from app.schemas import candidate_schemas, profburo_schemas

from app.oauth2 import is_current_user_admin

router = APIRouter(prefix="/candidates", tags=["Кандидаты"])


@router.get("/", response_model=List[candidate_schemas.CandidateOut])
@cache(namespace="candidates")
async def get_candidates(db: Session = Depends(get_db)):
    candidates = db.query(models.Candidate).all()
    return candidates


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=candidate_schemas.CandidateOut,
)
async def create_candidate(
        candidate: candidate_schemas.CandidateCreate,
        current_user_admin=Depends(is_current_user_admin),
        db: Session = Depends(get_db),
):
    new_candidate = models.Candidate(**candidate.dict())
    db.add(new_candidate)
    db.commit()

    await FastAPICache.clear()

    db.refresh(new_candidate)

    return new_candidate


@router.patch("/{id}", response_model=candidate_schemas.CandidateOut)
async def update_candidate(
        id: int,
        new_data: candidate_schemas.CandidateUpdate,
        current_user_admin=Depends(is_current_user_admin),
        db: Session = Depends(get_db),
):
    candidate_query = db.query(models.Candidate).filter(models.Candidate.id == id)
    candidate = candidate_query.first()

    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Кандидат с ID {id} не найден.")
    updated_data = new_data.dict(exclude_unset=True)  # убираем None-поля

    if updated_data:
        candidate_query.update(updated_data)
        db.commit()
        db.refresh(candidate)

        await FastAPICache.clear()

    return candidate


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
        id: int,
        current_user_admin=Depends(is_current_user_admin),
        db: Session = Depends(get_db),
):
    candidate = db.query(models.Candidate).filter(models.Candidate.id == id).first()
    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Кандидат с ID {id} не найден.",
        )
    db.delete(candidate)
    db.commit()

    await FastAPICache.clear()

    return {"message:": "Кандидат успешно удален."}

@router.get('/profburo', response_model=List[profburo_schemas.MemberOut])
@cache(namespace='candidates/profburo')
async def get_profburo(db: Session = Depends(get_db)):
    profburo = db.query(models.ProfburoMember).all()
    return profburo


@router.post('/profburo', status_code=status.HTTP_201_CREATED, response_model=profburo_schemas.MemberOut)
async def create_profburo_member(new_data: profburo_schemas.MemberCreate, db: Session = Depends(get_db),
                                 current_user_admin=Depends(is_current_user_admin)):
    new_member = models.ProfburoMember(**new_data.dict())
    db.add(new_member)
    db.commit()

    db.refresh(new_member)

    await FastAPICache.clear(namespace='candidates/profburo')

    return new_member


@router.patch('/profburo/{id}', response_model=profburo_schemas.MemberOut)
async def update_profburo_member(id: int, update_data: profburo_schemas.MemberUpdate, db: Session = Depends(get_db),
                                 current_user_admin=Depends(is_current_user_admin)):
    member_query = db.query(models.ProfburoMember).filter(models.ProfburoMember.id == id)
    member = member_query.first()

    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Член профсоюза с ID {id} не найден.')

    updated_data = update_data.dict(exclude_unset=True)

    if updated_data:
        member_query.update(updated_data, synchronize_session=False)
        db.commit()
        db.refresh(member)

        await FastAPICache.clear(namespace='candidates/profburo')

    return member


@router.delete('/profburo/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_profburo_member(id: int, db: Session = Depends(get_db),
                                 current_user_admin=Depends(is_current_user_admin)):
    member = db.query(models.ProfburoMember).filter(models.ProfburoMember.id == id).first()

    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Член профбюро с ID {id} не найден')

    db.delete(member)
    db.commit()

    await FastAPICache.clear(namespace='candidates/profburo')

    return member
