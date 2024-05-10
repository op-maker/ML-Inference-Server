import os
from transformers import AutoTokenizer, pipeline
from optimum.onnxruntime import ORTModelForQuestionAnswering

def load_model_and_tokenizer():
    model = ORTModelForQuestionAnswering.from_pretrained("optimum/roberta-base-squad2")
    tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
    device = os.getenv("DEVICE", "cpu")
    pipe = pipeline("question-answering", model=model, tokenizer=tokenizer, device=device)
    return pipe, (model, tokenizer)

def predict_qa(question, context, pipeline):
    pred = pipeline(question, context)
    return pred


# print(predict_qa(
#     "What's my name?", 
#     "My name is Philipp and I live in Nuremberg.",
#     load_model_and_tokenizer()[0]
#     ))

# print(predict_qa(
#     "Why is model conversion important?", 
#     "The option to convert models between FARM and transformers gives freedom to the user and let people easily switch between frameworks.",
#     load_model_and_tokenizer()[0]
#     ))