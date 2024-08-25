from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import models
from database import get_db
from schemas import candidate_schemas

from oauth2 import is_current_user_admin

router = APIRouter(prefix="/candidates", tags=["Кандидаты"])


@router.get('/', response_model=list(candidate_schemas.CandidateOut))
async def get_candidates(db: Session = Depends(get_db)):
    candidates = db.query(models.Candidate).all()
    return candidates


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=candidate_schemas.CandidateOut)
async def create_candidate(candidate: candidate_schemas.CandidateCreate,
                           current_user_admin = Depends(is_current_user_admin),
                           db: Session = Depends(get_db)):
    new_candidate = models.Candidate(**candidate.dict())
    db.add(new_candidate)
    db.commit()

    db.refresh(new_candidate)

    return new_candidate


@router.patch('/{id}')
async def update_candidate(id: int, new_data: candidate_schemas.CandidateUpdate,
                           current_user_admin = Depends(is_current_user_admin),
                           db: Session = Depends(get_db)):
    candidate_query = db.query(models.Candidate).filter(models.Candidate.id == id)
    candidate = candidate_query.first()

    if candidate is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Кандидат с ID {id} не найден.")

    updated_data = new_data.dict(exclude_unset=True)  # убираем None-поля

    if updated_data:
        candidate_query.update(updated_data)
        db.commit()
        db.refresh(candidate)

    return candidate


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(id: int, current_user_admin = Depends(is_current_user_admin),
                           db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).filter(models.Candidate.id == id).first()
    if candidate is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Кандидат с ID {id} не найден.")
    db.delete(candidate)
    db.commit()
    return {'message:': 'Кандидат успешно удален.'}
