from typing import List, Optional
from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    features: List[float] = Field(
        ...,
        description="单个样本特征",
        example=[5.1, 3.5, 1.4, 0.2],
    )


class PredictResponse(BaseModel):
    label: int
    class_name: str
    probability: Optional[List[float]] = None


class BatchPredictRequest(BaseModel):
    samples: List[List[float]] = Field(
        ...,
        description="多个样本，每个样本是一组特征",
        example=[
            [5.1, 3.5, 1.4, 0.2],
            [6.2, 3.4, 5.4, 2.3],
        ],
    )


class BatchPredictResponse(BaseModel):
    results: List[PredictResponse]