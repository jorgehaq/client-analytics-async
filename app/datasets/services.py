import os
import shutil
import pandas as pd
import numpy as np
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.datasets.models import Dataset
from app.datasets.schemas import DatasetResponse
from app.core.config import UPLOAD_DIR

ALLOWED_EXTENSIONS = ["csv", "xlsx"]

def save_dataset(db: Session, file: UploadFile, user_id: int) -> DatasetResponse:
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    ext = file.filename.split(".")[-1]
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    relative_path = f"datasets/{file.filename}"

    df = pd.read_csv(file.file, nrows=1)
    columns_names = df.columns.tolist()
    if not columns_names:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "File has not columns"})

    file.file.seek(0)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    dataset = Dataset(
        filename=file.filename,
        file_type=file.content_type,
        file_size=os.path.getsize(file_path),
        file_path=relative_path,
        columns=columns_names,
        user_id=user_id
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return dataset


def dataset_preview_services(db: Session, dataset_id: int, user_id: int, output_format: str):
    
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id, Dataset.user_id == user_id).first()

    if not dataset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    
    file_path = os.path.join(UPLOAD_DIR, dataset.filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:   
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")

        if output_format.lower() == "records":
            return df.to_dict(orient="records")

        return {
            "columns": df.columns.tolist(),
            "rows": df.values.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))   
    

def dataset_summary_services(db: Session, dataset_id: int, user_id: int):
    
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id, Dataset.user_id == user_id).first()

    if not dataset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    
    file_path = os.path.join(UPLOAD_DIR, dataset.filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:   
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")

        summary = df.describe(include="all").replace({np.nan: None}).to_dict()

        return {
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))   
    