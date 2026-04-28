import json

FILENAME = "tasks.json"

def load_tasks():
    """
    Пытается прочитать файл tasks.json. Если файла нет или он пустой - возвращает пустой список
    """
    try:
        with open(FILENAME, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
            return tasks
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    """
    Получает список задач и сохраняет его в файл tasks.json
    """
    with open(FILENAME, 'w', encoding='utf-8') as f:
        '''
        json.dump превращает список в текст и записыает в файл. ensure_ascii=False - разрешает русские буквы.
        indent=4 - делает красивые отступы в файле, делает текст читаемым
        '''
        json.dump(tasks, f, ensure_ascii=False, indent=4)

#Блок проверки
if __name__ == "__main__":
    print("Проверяем работу storage.py")
    current = load_tasks()
    print(f"Сейчас в хранилище: {current}")

    test_task =[{"id":1, "text": "Научиться читать JSON", "done": False}]
    save_tasks(test_task)   
    print("Сохранили тестовую задачу. Проверь, появился ли файл tasks.json слева!")