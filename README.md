# ML-Inference-Server with Celery queue, Redis and Traefik

It is a project of inference server for Question-Answering task with ONNX Runtime optimized model, FastAPI, Gradio as the frontend part, Celery as the task queue, Redis as the Celery-backend and Traefik as the reverse proxy and load-balancer. All services are packaged in Docker-containers. 

An example of work is located below. 


![image](https://github.com/op-maker/ML-Inference-Server/assets/80627278/08dd6fa4-41be-4e71-be65-cbf7de0f7b10)


## Work description
When you click the `Submit` button on the frontend, a Celery task is first added for back-end processing and task ID is returned. 

After that, when async inference is ready, it returns the answer to the given question and context, as well as the score of that answer. 

Traefik is responsible for routing and load balancing requests for the back-end part.

## Launch instructions

1. Clone the repo: `git clone https://github.com/op-maker/ML-Inference-Server.git`
2. Create images in the docker compose: `docker-compose build`
3. Run containers: `docker-compose up`
4. Follow the link in your browser: http://127.0.0.1:7860/

It also generates a public link for your inference-service by default. 

OpenAPI documentation is available at http://127.0.0.1:8081/docs.

To view the Traefik dashboard of your configuration, please go to http://127.0.0.1:8080

![image](https://github.com/op-maker/ML-Inference-Server/assets/80627278/a75a8acd-12ee-402e-a5d2-ea87a3c147a9)
