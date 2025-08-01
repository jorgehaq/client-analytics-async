from fastapi import APIRouter, Depends, UploadFile, File, Query
from app.datasets.schemas import DatasetResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.datasets.services import save_dataset, dataset_preview_services, dataset_summary_services
from app.accounts.services import get_current_user


router = APIRouter(prefix="/datasets", tags=["datasets"])

@router.post("/upload", response_model=DatasetResponse)
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    return save_dataset(db, file, user.id)

@router.get("/{pk}/preview")
async def preview_dataset(pk: int, 
                          output: str = Query("", description="Output format"), 
                          db: Session = Depends(get_db),
                          user=Depends(get_current_user)):
    return dataset_preview_services(db, pk, user.id, output)

@router.get("/{pk}/summary")
async def summary_dataset(pk: int,
                          db: Session = Depends(get_db),
                          user=Depends(get_current_user)):
    return dataset_summary_services(db, pk, user.id)