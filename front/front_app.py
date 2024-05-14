import gradio as gr
import requests
import json
import os
from retrying import retry
from typing import Dict, Any

STATUS_CREATED = 201
STATUS_PENDING = 202

import time

@retry(stop_max_attempt_number=10, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def get_result(task_id: str) -> Dict[Any, Any]:
    start = time.time()
    response = requests.get(f"http://127.0.0.1:8081/api/task/{task_id}")
    # response = requests.get(f"http://web/api/task/{task_id}")
    if response.status_code == STATUS_PENDING:
        raise gr.Error("Task on progress")

    return response.json()

def predict_answer(question: str, context: str):
    
    input = {'question': question, 'context': context}
    response = requests.post(
        "http://127.0.0.1:8081/api/predict",
        # "http://web/api/predict",
        data = json.dumps(input),
        )
    
    if response.status_code == 400:
        raise gr.Error("Please, fill the empty fields")

    task_id = response.json()['id'] if response.status_code == STATUS_CREATED else None
    
    data = get_result(task_id)

    if data['status'] != 'SUCCESS':
        print("err", data)
        raise gr.Error(f"Not successed task response: {data['error']}")

    out = data["result"]
    
    return out["answer"], out["score"]


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
    """
    # Inference server for Question-Answering
    Start typing below to see the result.
    """
    )
    with gr.Row() as row:
        with gr.Column():
            question_txt = gr.Textbox(label="Type question")
            context_txt = gr.Textbox(label="Type context for question", lines=2)
            with gr.Row() as row:
                btn = gr.Button(value="Submit")
                clear_btn = gr.ClearButton(value="Clear")
        with gr.Column():
            ans_txt = gr.Textbox(value="", label="Answer")
            score_txt = gr.Textbox(value="", label="Score")
    btn.click(
        predict_answer, 
        inputs=[question_txt, context_txt], 
        outputs=[ans_txt, score_txt]
    )
    clear_btn.click(lambda: [None, None], outputs=[question_txt, context_txt])

if __name__ == "__main__":
    share_property = os.getenv("IS_SHAREABLE", False)
    demo.queue(default_concurrency_limit=10).launch(
        share=share_property,
        server_name="0.0.0.0",
        server_port=7860,
    )