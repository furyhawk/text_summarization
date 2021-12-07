from pydantic import BaseModel
from typing import List, Optional, Any
from logging.config import dictConfig
import logging

from rouge_score import rouge_scorer

from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk import tokenize
import numpy as np

from app.core.config import LogConfig, get_settings

MODELS = get_settings().MODELS


class ModelOutput(BaseModel):
    model: List[str] = []


class PredictionInput(BaseModel):
    text: str
    reference: str
    modelId: str


class PredictionOutput(BaseModel):
    summarized: str
    metrics: str


class TextSummaryModel():
    model: Optional[Any]
    targets: Optional[List[str]]

    def __init__(self):
        dictConfig(LogConfig().dict())
        logger = logging.getLogger("app")
        self.logger = logger

    def load_model(self):
        """Loads the model"""
        self.logger.info("Preloading transformer pipleine")
        nltk.download('punkt')

    def get_models(self) -> ModelOutput:
        model = MODELS
        return ModelOutput(model=model)

    def predict(self, input: PredictionInput) -> PredictionOutput:
        """Summarize text input(x) to (y)"""

        self.logger.info(input.text)

        # Parameters
        target = input.reference
        modelId = input.modelId

        min_length = get_settings().MIN_LENGTH
        max_length = get_settings().MAX_LENGTH
        headline_min_length = get_settings().HEADLINE_MIN_LENGTH
        headline_max_length = get_settings().HEADLINE_MAX_LENGTH

        prediction = 'No result'

        if modelId == 'TFIDF':
            prediction = self.tfidf_summary(
                text=input.text, num_summary_sentence=1)

        # Print summarized text
        self.logger.info(prediction)
        scorer = rouge_scorer.RougeScorer(
            ['rouge1', 'rouge2', 'rougeL', 'rougeLsum'], use_stemmer=True)
        # Calculates rouge scores between the target and prediction.
        scores = scorer.score(target, prediction)
        self.print_rouge_score(scores)

        return PredictionOutput(summarized=prediction, metrics=self.output_rouge_score(scores))

    def print_rouge_score(self, rouge_score):
        """format and print rouge score"""
        for k, v in rouge_score.items():
            print(k, 'Precision:', "{:.2f}".format(v.precision), 'Recall:', "{:.2f}".format(
                v.recall), 'fmeasure:', "{:.2f}".format(v.fmeasure))

    def output_rouge_score(self, rouge_score):
        """format and output rouge score"""
        output = ''
        for k, v in rouge_score.items():
            output += ' ' + k + ' Precision:' + "{:.2f}".format(v.precision) + ' Recall:' + "{:.2f}".format(
                v.recall) + ' fmeasure:' + "{:.2f}".format(v.fmeasure) + ' '
        return output

    def tfidf_summary(self, text, num_summary_sentence):
        """tfidf summary"""
        summary_sentence = ''
        sentences = tokenize.sent_tokenize(text)
        tfidfVectorizer = TfidfVectorizer()
        words_tfidf = tfidfVectorizer.fit_transform(sentences)
        sentence_sum = words_tfidf.sum(axis=1)
        important_sentences = np.argsort(sentence_sum, axis=0)[::-1]
        for i in range(0, len(sentences)):
            if i in important_sentences[:num_summary_sentence]:
                summary_sentence = summary_sentence + sentences[i]

        return summary_sentence


# Create Singleton
textSummaryModel = TextSummaryModel()


def get_model():

    return textSummaryModel
