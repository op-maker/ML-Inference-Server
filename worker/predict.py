import os
from transformers import AutoTokenizer, pipeline
from optimum.onnxruntime import ORTModelForQuestionAnswering

from celery import Celery

papp = Celery(
    "predict",
    # "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

def load_model_and_tokenizer():
    model = ORTModelForQuestionAnswering.from_pretrained("optimum/roberta-base-squad2")
    tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
    device = os.getenv("DEVICE", "cpu")
    pipe = pipeline("question-answering", model=model, tokenizer=tokenizer, device=device)
    return pipe, (model, tokenizer)

pipe, _ = load_model_and_tokenizer()

@papp.task(name="predict_qa")
def predict_qa(question, context):
    pred = pipe(question, context)
    return pred

