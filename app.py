from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from storage import load_tasks, save_tasks

app = FastAPI()

def get_next_id(tasks: list) -> int:
    if not tasks:
        return 1
    max_id = max(task.get("id", 0) for task in tasks)
    return max_id + 1

@app.get("/")
async def read_tasks():
    tasks = load_tasks()

    # Начинаем HTML-страницу (стили + заголовок + форма добавления)
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Мой ToDo</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial; max-width: 600px; margin: 50px auto; }
            .task { padding: 10px; border-bottom: 1px solid #eee; display: flex; align-items: center; }
            .task span { flex-grow: 1; }
            .task form { display: inline; margin-left: 10px; }
            button { background: none; border: none; cursor: pointer; font-size: 1.2em; }
            .add-form { margin: 20px 0; }
            .add-form input[type="text"] { padding: 8px; width: 70%; }
        </style>
    </head>
    <body>
        <h1>📝 Мои задачи</h1>

        <form class="add-form" action="/add" method="post">
            <input type="text" name="task_text" placeholder="Что нужно сделать?" required>
            <br>
            <label>Дедлайн: <input type="date" name="deadline"></label>
            <br>
            <label>Приоритет:
                <select name="priority">
                    <option value="">-- Не выбрано --</option>
                    <option value="Высокий">Высокий</option>
                    <option value="Средний">Средний</option>
                    <option value="Низкий">Низкий</option>
                </select>
            </label>
            <br>
            <button type="submit">➕ Добавить</button>
        </form>

        <div class="tasks">
    """

    # Для каждой задачи создаём блок с кнопками-формами
    for task in tasks:
        task_id = task.get("id", 0)
        task_text = task.get("text", "")
        task_done = task.get("done", False)

               # Текст задачи с зачёркиванием, если выполнена
        display_text = f"<s>{task_text}</s>" if task_done else task_text

        # Дополнительная информация: дедлайн и приоритет
        extra_info = ""
        if task.get("deadline"):
            extra_info += f" ⏰ {task['deadline']}"
        if task.get("priority"):
            extra_info += f" ⭐ {task['priority']}"

        html += f"""
            <div class="task">
                <span>{display_text}{extra_info}</span>
                <form action="/complete/{task_id}" method="post">
                    <button type="submit" title="Выполнено / Не выполнено">✅</button>
                </form>
                <form action="/delete/{task_id}" method="post">
                    <button type="submit" title="Удалить">🗑</button>
                </form>
            </div>
        """

    # Закрываем HTML
    html += f"""
        </div>
        <p><small>Всего задач: {len(tasks)}</small></p>
    </body>
    </html>
    """

    return HTMLResponse(content=html)

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