from starlette.testclient import TestClient

from app import app
import time

client = TestClient(app)


def run_test(
    question: str, 
    context: str, 
    expected_answer: str, 
    test_app,
    tries_count: int = 40
):
    first_response = test_app.post(
        "api/predict",
        json={
            "question": question,
            "context": context,
        }
    )
    task_id = first_response.json()['id']

    tries = 0
    while True:
        tries += 1
        response = test_app.get(f"api/task/{task_id}")
        # if status is not pending
        if response.status_code != 202 or tries >= tries_count:
            break
        time.sleep(0.2)

    # check if the response status is successful
    assert response.status_code == 200
    output = response.json()["result"]
    assert output["answer"] == expected_answer


def test_predict(test_app):
    
    question1 = "What's my name?"
    context1 = "My name is Philipp and I live in Nuremberg"
    exp_answer1 = "Philipp"

    run_test(question1, context1, exp_answer1, test_app)
    
    question2 = "Why is model conversion important?"
    context2 = "The option to convert models between FARM and transformers gives freedom to the user and let people easily switch between frameworks."
    exp_answer2 = "gives freedom to the user"
    
    run_test(question2, context2, exp_answer2, test_app)
