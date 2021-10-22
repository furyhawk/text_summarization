import uvicorn
import os
import logging
from typing import List, Optional, Tuple

from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rouge_score import rouge_scorer

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import tokenize
import numpy as np


class PredictionInput(BaseModel):
    text: str
    reference: str
    modelId: str


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

        gold_standard = input.reference
        modelId = input.modelId

        summary = 'No result'
        if modelId == 'Transformer':
            summary = self.transformer_summary(
                text=input.text, min_length=75, max_length=300)
        if modelId == 'TFIDF':
            summary = self.tfidf_summary(
                text=input.text, num_summary_sentence=3)
        if modelId == 'T5':
            summary = self.t5_summary(
                text=input.text, min_length=75, max_length=300)
        if modelId == 'Finetuned':
            summary = self.finetuned_summary(
                text=input.text, min_length=75, max_length=300)

        # Print summarized text
        logger.info(summary)
        scorer = rouge_scorer.RougeScorer(
            ['rouge1', 'rougeL'], use_stemmer=True)
        scores = scorer.score(gold_standard, summary)
        self.print_rouge_score(scores)

        return PredictionOutput(summarized=summary, metrics=str(scores))

    def print_rouge_score(self, rouge_score):
        for k, v in rouge_score.items():
            print(k, 'Precision:', "{:.2f}".format(v.precision), 'Recall:', "{:.2f}".format(
                v.recall), 'fmeasure:', "{:.2f}".format(v.fmeasure))

    def tfidf_summary(self, text, num_summary_sentence):
        summary_sentence = ''
        sentences = tokenize.sent_tokenize(text)
        tfidfVectorizer = TfidfVectorizer()
        words_tfidf = tfidfVectorizer.fit_transform(sentences)
        sentence_sum = words_tfidf.sum(axis=1)
        important_sentences = np.argsort(sentence_sum, axis=0)[::-1]
        for i in range(0, len(sentences)):
            if i in important_sentences[:num_summary_sentence]:
                summary_sentence = summary_sentence + sentences[i]

        print(summary_sentence)
        return summary_sentence

    def transformer_summary(self, text, min_length=75, max_length=300):
        summarized = self.model(
            text, min_length=min_length, max_length=max_length)
        return summarized[0]["summary_text"]

    def t5_summary(self, text, min_length=75, max_length=300):
        model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
        tokenizer = AutoTokenizer.from_pretrained("t5-base")

        # T5 uses a max_length of 512 so we cut the article to 512 tokens.
        inputs = tokenizer("summarize: " + text,
                           return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(inputs["input_ids"], max_length,
                                 min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(outputs[0])                                 
        print(summary)
        return summary

    def finetuned_summary(self, text, min_length=75, max_length=300):
        model = AutoModelForSeq2SeqLM.from_pretrained("furyhawk/t5-small-finetuned-xsum")
        tokenizer = AutoTokenizer.from_pretrained("furyhawk/t5-small-finetuned-xsum")

        # T5 uses a max_length of 512 so we cut the article to 512 tokens.
        inputs = tokenizer("summarize: " + text,
                           return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(inputs["input_ids"], max_length,
                                 min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(outputs[0])                                 
        print(summary)
        return summary

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
    logger.info("start")
    # Initialize the HuggingFace summarization pipeline
    textsummary_model.load_model()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
