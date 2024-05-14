from fastapi import FastAPI, HTTPException

import uvicorn
from pydantic import BaseModel
from typing import Optional, Any
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED
)

from celery import Celery, states


# from model import load_model_and_tokenizer, predict_qa


app = FastAPI()

pred_app = Celery(
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

class QuestionParams(BaseModel):
    question: str
    context: str

class QuestionResponse(BaseModel):
    score: float
    start: int
    end: int
    answer: str

class TaskResult(BaseModel):
    id: str
    status: str
    error: Optional[str] = None
    result: Optional[Any] = None


@app.get("/")
def root():
    '''
    Create a route
    '''
    return {"message": "Service for question-answering task"}

pipeline = None

# @app.on_event("startup")
# def startup_loading():
#     '''
#     Register the pipeline to run during startup
#     '''
#     global pipeline
#     pipeline, _ = load_model_and_tokenizer()

@app.post("/api/predict", status_code=HTTP_201_CREATED)
def predict_answer(q_params: QuestionParams): #-> QuestionResponse:
    '''
    Make a prediction based on context
    '''
    # needed for tests
    # if 'pipeline' not in locals():
    #     pipeline, _ = load_model_and_tokenizer()

    if not q_params.question:
        raise HTTPException(status_code=400, detail="Question text is empty! Please, fill it.")

    if not q_params.context:
        raise HTTPException(status_code=400, detail="Context is empty! Please, fill it.")
    
    task = pred_app.send_task(
        name="predict_qa",
        # name="papp",
        kwargs={"question": q_params.question, "context": q_params.context}
    )

    return {"id": task.id}


@app.get("/api/task/{task_id}")
def get_result(task_id: str):

    result = pred_app.AsyncResult(task_id)

    output = TaskResult(
        id=task_id,
        status=result.state,
        error=str(result.info) if result.failed() else None,
        result=result.get() if result.state == states.SUCCESS else None
    )

    return JSONResponse(
        status_code= HTTP_202_ACCEPTED if result.state == states.PENDING else HTTP_200_OK,
        content=output.dict()
    )

    # tmp = predict_qa(q_params.question, q_params.context, pipeline)
    # answer = QuestionResponse(
    #     score=tmp['score'],
    #     start=tmp['start'],
    #     end=tmp['end'],
    #     answer=tmp['answer']
    # )
    
    # return answer
                

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
   


