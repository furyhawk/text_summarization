import uvicorn
import os
import logging
from typing import List, Optional, Tuple

from transformers import pipeline
from fastapi import FastAPI, Depends, status
from pydantic import BaseModel


class PredictionInput(BaseModel):
    text: str


class PredictionOutput(BaseModel):
    summarized: str

class TextSummaryModel:
    model: Optional[pipeline]
    targets: Optional[List[str]]

    def load_model(self):
        """Loads the model"""
        # Initialize the HuggingFace summarization pipeline
        summarizer = pipeline("summarization")
        self.model = summarizer
        logger.info(self.model)

    def predict(self, input: PredictionInput) -> PredictionOutput:
        """Runs a prediction"""
        if not self.model:
            raise RuntimeError("Model is not loaded")

        logger.info(input.text)
        summarized = self.model(input.text, min_length=75, max_length=300)
        # Print summarized text
        logger.info(summarized)

        return PredictionOutput(summarized=summarized[0]["summary_text"])

app = FastAPI(debug=True)
logger = logging.getLogger("app")
textsummary_model = TextSummaryModel()

@app.post("/prediction", response_model=PredictionOutput)
# async def prediction(predictionInput: PredictionInput):
#     return textsummary_model.predict(predictionInput)
def prediction(
    output: PredictionOutput = Depends(textsummary_model.predict),
) -> PredictionOutput:
    return output

@app.on_event("startup")
async def startup():
    # Initialize the HuggingFace summarization pipeline
    # summarizer = pipeline("summarization")
    # self.model = summarizer
    # logger = logging.getLogger("uvicorn.access")
    # handler = logging.StreamHandler()
    # handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    # logger.addHandler(handler)
    logger.info("start")
    textsummary_model.load_model()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)