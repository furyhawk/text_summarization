from pydantic import BaseModel
from typing import List, Optional, Any
from logging.config import dictConfig
import logging

from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
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

        """Default init Google T5 huggingface transformer pipeline summary task"""
        self.model = AutoModelForSeq2SeqLM.from_pretrained("furyhawk/t5-base-finetuned-bbc-headline")
        self.tokenizer = AutoTokenizer.from_pretrained("furyhawk/t5-base-finetuned-bbc-headline")

    def get_models(self) -> ModelOutput:
        model = MODELS
        return ModelOutput(model=model)

    def predict(self, input: PredictionInput) -> PredictionOutput:
        """Summarize text input(x) to (y)"""
        if not self.model:
            raise RuntimeError("Model is not loaded")

        self.logger.info(input.text)

        # Parameters
        target = input.reference
        modelId = input.modelId

        min_length = get_settings().MIN_LENGTH
        max_length = get_settings().MAX_LENGTH
        headline_min_length = get_settings().HEADLINE_MIN_LENGTH
        headline_max_length = get_settings().HEADLINE_MAX_LENGTH

        prediction = 'No result'

        if modelId == 'Transformer':
            # Initialize the HuggingFace summarization pipeline
            summarizer = pipeline("summarization")
            self.model = summarizer
            prediction = self.transformer_summary(
                text=input.text, min_length=min_length, max_length=max_length)
        if modelId == 'TFIDF':
            prediction = self.tfidf_summary(
                text=input.text, num_summary_sentence=1)
        if modelId == 'T5':
            t5model="t5-base"
            self.model = AutoModelForSeq2SeqLM.from_pretrained(t5model)
            self.tokenizer = AutoTokenizer.from_pretrained(t5model)
            prediction = self.t5_summary(
                                         text=input.text,
                                         min_length=min_length, max_length=max_length)
        if modelId == 'Finetuned':
            t5model="furyhawk/t5-base-finetuned-bbc"
            self.model = AutoModelForSeq2SeqLM.from_pretrained(t5model)
            self.tokenizer = AutoTokenizer.from_pretrained(t5model)
            prediction = self.t5_summary(
                                         text=input.text,
                                         min_length=min_length, max_length=max_length)
        if modelId == 'Headline':
            t5model="furyhawk/t5-base-finetuned-bbc-headline"
            self.model = AutoModelForSeq2SeqLM.from_pretrained(t5model)
            self.tokenizer = AutoTokenizer.from_pretrained(t5model)
            prediction = self.t5_summary(
                                         text=input.text,
                                         min_length=headline_min_length, max_length=headline_max_length)

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

    def transformer_summary(self, text, min_length=3, max_length=512):
        """default huggingface transformer pipeline summary task"""
        summarized = self.model(
            text, min_length=min_length, max_length=max_length)
        return summarized[0]["summary_text"]

    def t5_summary(self, text="", min_length=3, max_length=512):
        """Google T5 huggingface transformer pipeline summary task"""

        # T5 uses a max_length of 512 so we cut the article to 512 tokens.
        inputs = self.tokenizer("summarize: " + text,
                           return_tensors="pt", max_length=512, truncation=True)
        outputs = self.model.generate(input_ids=inputs["input_ids"], attention_mask=inputs['attention_mask'],
                                 max_length=max_length, min_length=min_length, length_penalty=0.1,
                                 num_beams=4, early_stopping=True)
        summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return summary


# Create Singleton
textSummaryModel = TextSummaryModel()


def get_model():

    return textSummaryModel
