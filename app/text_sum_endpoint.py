import uvicorn
import os
import logging
from typing import List, Optional, Tuple

from transformers import pipeline
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rouge_score import rouge_scorer


class PredictionInput(BaseModel):
    text: str
    reference: str


class PredictionOutput(BaseModel):
    summarized: str
    metrics: str


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
        summary = summarized[0]["summary_text"]
        gold_standard = input.reference
        # Print summarized text
        logger.info(summary)
        scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
        scores = scorer.score(gold_standard, summary)
        print(scores)
        # self.print_rouge_score(scores)

        return PredictionOutput(summarized=summary, metrics=str(scores))

    def print_rouge_score(rouge_score):
        for k, v in rouge_score.items():
            print(k, 'Precision:', "{:.2f}".format(v.precision), 'Recall:', "{:.2f}".format(
                v.recall), 'fmeasure:', "{:.2f}".format(v.fmeasure))


app = FastAPI(debug=True)
logger = logging.getLogger("app")
textsummary_model = TextSummaryModel()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
