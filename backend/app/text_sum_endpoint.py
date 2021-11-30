import uvicorn
import logging

from fastapi import FastAPI, Depends
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.models.models import TextSummaryModel, ModelOutput, PredictionOutput

app = FastAPI()
logger = logging.getLogger("app")
textsummary_model = TextSummaryModel()

@ app.get("/models", response_model=ModelOutput)
async def models(
    output: ModelOutput = Depends(textsummary_model.get_model),
) -> ModelOutput:
    return output

@ app.post("/prediction", response_model=PredictionOutput)
def prediction(
    output: PredictionOutput = Depends(textsummary_model.predict),
) -> PredictionOutput:
    return output

@ app.on_event("startup")
async def startup():
    # Initialize the HuggingFace summarization pipeline
    textsummary_model.load_model()

app.add_middleware(GZipMiddleware)
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
