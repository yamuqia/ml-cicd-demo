from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.schemas import (
    PredictRequest,
    PredictResponse,
    BatchPredictRequest,
    BatchPredictResponse,
)
from app.model_service import ModelService


model_service = ModelService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    服务启动时执行 yield 前面的代码；
    服务关闭时执行 yield 后面的代码。

    这里用来在 API 启动时加载模型。
    """
    model_service.load_model()
    yield


app = FastAPI(
    title="ML CICD Demo API",
    description="A minimal machine learning inference service for CI/CD practice.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "message": "ML CICD Demo API is running.",
        "docs": "/docs",
        "health": "/health",
        "predict": "/predict",
        "batch_predict": "/batch_predict",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model_service.model is not None,
    }


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    try:
        return model_service.predict(request.features)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch_predict", response_model=BatchPredictResponse)
def batch_predict(request: BatchPredictRequest):
    try:
        results = model_service.batch_predict(request.samples)
        return {"results": results}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))