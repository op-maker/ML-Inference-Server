from starlette.testclient import TestClient

from app import app
from model import load_model_and_tokenizer

client = TestClient(app)


def test_predict(test_app):
    
    response1 = test_app.post(
        "api/predict",
        json={
            "question": "What's my name?",
            "context": "My name is Philipp and I live in Nuremberg",
        }
    )
    assert response1.status_code == 200
    assert response1.json()["answer"] == "Philipp"

    response2 = test_app.post(
        "api/predict",
        json={
            "question": "Why is model conversion important?",
            "context": "The option to convert models between FARM and transformers gives freedom to the user and let people easily switch between frameworks.",
        }
    )
    assert response2.status_code == 200
    assert response2.json()["answer"] == "gives freedom to the user"