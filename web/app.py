from fastapi import FastAPI, HTTPException

import uvicorn
from pydantic import BaseModel


from model import load_model_and_tokenizer, predict_qa

app = FastAPI()

class QuestionParams(BaseModel):
    question: str
    context: str

class QuestionResponse(BaseModel):
    score: float
    start: int
    end: int
    answer: str


@app.get("/")
def root():
    '''
    Create a route
    '''
    return {"message": "Service for question-answering task"}

pipeline = None

@app.on_event("startup")
def startup_loading():
    '''
    Register the pipeline to run during startup
    '''
    global pipeline
    pipeline, _ = load_model_and_tokenizer()

@app.post("/api/predict")
def predict_answer(q_params: QuestionParams) -> QuestionResponse:
    '''
    Make a prediction based on context
    '''
    # needed for tests
    if 'pipeline' not in locals():
        pipeline, _ = load_model_and_tokenizer()

    if not q_params.question:
        raise HTTPException(status_code=400, detail="Question text is empty! Please, fill it.")

    if not q_params.context:
        raise HTTPException(status_code=400, detail="Context is empty! Please, fill it.")
    tmp = predict_qa(q_params.question, q_params.context, pipeline)
    answer = QuestionResponse(
        score=tmp['score'],
        start=tmp['start'],
        end=tmp['end'],
        answer=tmp['answer']
    )
    
    return answer
                

if __name__ == "__main__":
    """
    Server configurations
    """
    
    uvicorn.run(
        app="app:app",
        host="0.0.0.0", 
        port=80, 
        reload=True, 
        log_level="info",
    )
   


