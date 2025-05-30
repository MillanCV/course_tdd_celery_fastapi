import logging
import random

import requests
from celery.result import AsyncResult
from fastapi import FastAPI, Request, Body
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from project.users.router import users_router
from project.users.schemas import UserBody
from project.users.tasks import sample_task, task_process_notification


logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="project/users/templates")


def api_call(email: str):
    # used for testing a failed api call
    if random.choice([0, 1]):
        raise Exception("random processing error")

    # used for simulating a call to a third-party api
    requests.post("https://httpbin.org/delay/5")


@users_router.get("/form/")
def form_example_get(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@users_router.post("/form/")
def form_example_post(user_body: UserBody):
    task = sample_task.delay(user_body.email)
    return JSONResponse({"task_id": task.task_id})


@users_router.get("/task_status/")
def task_status(task_id: str):
    task = AsyncResult(task_id)
    state = task.state

    if state == "FAILURE":
        error = str(task.result)
        response = {
            "state": state,
            "error": error,
        }
    else:
        response = {
            "state": state,
        }
    return JSONResponse(response)


@users_router.post("/webhook_test/")
def webhook_test():
    if not random.choice([0, 1]):
        # mimic an error
        raise Exception()

    # blocking process
    requests.post("https://httpbin.org/delay/5")
    return "pong"


@users_router.post("/webhook_test_async/")
def webhook_test_async():
    task = task_process_notification.delay()
    print(task.id)
    return "pong"


@users_router.get("/form_ws/")
def form_ws_example(request: Request):
    return templates.TemplateResponse("form_ws.html", {"request": request})


@users_router.get("/form_socketio/")
def form_socketio_example(request: Request):
    return templates.TemplateResponse("form_socketio.html", {"request": request})
