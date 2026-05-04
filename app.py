from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from storage import load_tasks, save_tasks

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_next_id(tasks: list) -> int:
    if not tasks:
        return 1
    max_id = max(task.get("id", 0) for task in tasks)
    return max_id + 1

@app.get("/", response_class=HTMLResponse)
async def read_tasks(request: Request):
    tasks = load_tasks()
    return templates.TemplateResponse("index.html", {"tasks": tasks, "request": request})

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

@app.post("/add")
async def add_task(task_text: str = Form(...),
                    deadline: str = Form(""),
                    priority: str = Form("")
                    ):
    tasks = load_tasks()
    new_id = get_next_id(tasks)
    new_task = {
        "id": new_id,
        "text": task_text,
        "done": False,
        "deadline": deadline if deadline else None,
        "priority": priority if priority else None
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return RedirectResponse(url="/", status_code=303)

@app.post("/complete/{task_id}")
async def complete_task(task_id: int):
    tasks = load_tasks()
    found = False
    for task in tasks:
        if task.get("id") == task_id:
            task["done"] = not task.get("done", False)
            found = True
            break
    if found:
        save_tasks(tasks)
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{task_id}")
async def delete_task(task_id: int):
    tasks = load_tasks()
    filtered_tasks = [task for task in tasks if task.get("id") != task_id]
    save_tasks(filtered_tasks)
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)