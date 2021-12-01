from typing import List

from fastapi import APIRouter, Depends

from app.models.models import TextSummaryModel, get_model, ModelOutput, PredictionInput, PredictionOutput
from app.core.config import Settings, get_settings

model_router = APIRouter()

# @model_router.get("/")
# async def all() -> List[Post]:
#     return list(db.posts.values())


@model_router.get('/test')
def get_param_list(config: Settings = Depends(get_settings)):
    return config


@ model_router.get("/models", response_model=ModelOutput)
async def models(
    model: TextSummaryModel = Depends(get_model),
) -> ModelOutput:
    output: ModelOutput = model.get_models()
    return output


@ model_router.post("/prediction", response_model=PredictionOutput)
def prediction(
    request: PredictionInput,
    model: TextSummaryModel = Depends(get_model),
) -> PredictionOutput:
    output: PredictionOutput = model.predict(request)
    return output


@ model_router.on_event("startup")
async def startup():
    """Initialize the HuggingFace summarization pipeline"""
    get_model().load_model()
