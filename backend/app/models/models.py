from pydantic import BaseModel
from typing import List, Optional
import logging

from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from rouge_score import rouge_scorer

from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk import tokenize
import numpy as np

MODELS = ['Transformer', 'TFIDF', 'T5', 'Finetuned', 'Headline']
logger = logging.getLogger(__name__)


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
    logger: logger
    model: Optional[pipeline]
    targets: Optional[List[str]]

    def load_model(self):
        nltk.download('punkt')
        """Loads the model"""
        # Initialize the HuggingFace summarization pipeline
        summarizer = pipeline("summarization")
        self.model = summarizer

    def get_model(self) -> ModelOutput:
        model = MODELS
        return ModelOutput(model=model)

    def predict(self, input: PredictionInput) -> PredictionOutput:
        """Runs a prediction"""
        if not self.model:
            raise RuntimeError("Model is not loaded")

        # self.logger.info(input.text)

        # Parameters
        target = input.reference
        modelId = input.modelId

        min_length = 15
        max_length = 150
        headline_min_length = 7
        headline_max_length = 20

        prediction = 'No result'

        if modelId == 'Transformer':
            prediction = self.transformer_summary(
                text=input.text, min_length=min_length, max_length=max_length)
        if modelId == 'TFIDF':
            prediction = self.tfidf_summary(
                text=input.text, num_summary_sentence=1)
        if modelId == 'T5':
            prediction = self.t5_summary(t5model="t5-base",
                                         text=input.text,
                                         min_length=min_length, max_length=max_length)
        if modelId == 'Finetuned':
            prediction = self.t5_summary(t5model="furyhawk/t5-base-finetuned-bbc",
                                         text=input.text,
                                         min_length=min_length, max_length=max_length)
        if modelId == 'Headline':
            prediction = self.t5_summary(t5model="furyhawk/t5-base-finetuned-bbc-headline",
                                         text=input.text,
                                         min_length=min_length, max_length=max_length)

        # Print summarized text
        # self.logger.info(prediction)
        scorer = rouge_scorer.RougeScorer(
            ['rouge1', 'rouge2', 'rougeL', 'rougeLsum'], use_stemmer=True)
        # Calculates rouge scores between the target and prediction.
        scores = scorer.score(target, prediction)
        self.print_rouge_score(scores)

        return PredictionOutput(summarized=prediction, metrics=self.output_rouge_score(scores))

    def print_rouge_score(self, rouge_score):
        """format and print rouge score"""
        # output = ''
        for k, v in rouge_score.items():
            print(k, 'Precision:', "{:.2f}".format(v.precision), 'Recall:', "{:.2f}".format(
                v.recall), 'fmeasure:', "{:.2f}".format(v.fmeasure))
        # return output

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

        print(summary_sentence)
        return summary_sentence

    def transformer_summary(self, text, min_length=3, max_length=512):
        """default huggingface transformer pipeline summary task"""
        summarized = self.model(
            text, min_length=min_length, max_length=max_length)
        return summarized[0]["summary_text"]

    def t5_summary(self, t5model="t5-base", text="", min_length=3, max_length=512):
        model = AutoModelForSeq2SeqLM.from_pretrained(t5model)
        tokenizer = AutoTokenizer.from_pretrained(t5model)

        # T5 uses a max_length of 512 so we cut the article to 512 tokens.
        inputs = tokenizer("summarize: " + text,
                           return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(input_ids=inputs["input_ids"], attention_mask=inputs['attention_mask'],
                                 max_length=max_length, min_length=min_length, length_penalty=0.1,
                                 num_beams=4, early_stopping=True)
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return summary
