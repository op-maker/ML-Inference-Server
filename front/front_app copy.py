import gradio as gr
import requests
import json
import os






def predict_answer(question: str, context: str):
    
    input = {'question': question, 'context': context}
    response = requests.post(
        "http://web/api/predict",
        data = json.dumps(input),
        )
    
    if response.status_code == 400:
        raise gr.Error("Please, fill the empty fields")

    print(response.status_code)
    out = response.json()
        
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
    print('*' * 30)
    print(share_property)
    print('*' * 30)
    demo.queue(default_concurrency_limit=10).launch(
        share=share_property,
        server_name="0.0.0.0",
        server_port=7860,
    )