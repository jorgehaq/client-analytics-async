from pydantic import BaseModel
from typing import List, Dict, Any


class DatasetBase(BaseModel):
    filename: str
    file_type: str
    file_size: float
    file_path: str
    columns: List[str]

class DatasetResponse(DatasetBase):
    id: int

    class Config:
        orm_mode = True


class DatasetSummaryResponse(BaseModel):
    dataset: DatasetResponse
    summary: Dict[str, Dict[str, Any]]

    class Config:
        orm_mode = True
