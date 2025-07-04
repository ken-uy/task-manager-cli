import argparse
import json
import os
import sys

TASKS_FILE = "tasks.json"


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_tasks(tasks, description):
    new_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({"id": new_id, "task": description, "done": False})
    print(f"Added tasks [{new_id}]: {description}")


def list_tasks(tasks):
    if not tasks:
        print("No tasks found")
        return

    for task in tasks:
        status = "✅" if task["done"] else "❌"
        print(f"[{task['id']}] {status} {task['task']}")


def mark_done(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            print(f"Marked task [{task_id}] as done")
            return
    print(f"Task [{task_id}] not found")


def delete_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            print(f"Deleted tasks [{task_id}]")
            return
    print(f"Task [{task_id}] not found")


def clear_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump([], f, indent=2)
    print("Cleared all tasks")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--add", type=str)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--done", type=int)
    parser.add_argument("--delete", type=int)
    parser.add_argument("--clear", action="store_true")

    args = parser.parse_args()

    if args.clear:
        clear_tasks()
        sys.exit(0)

    tasks = load_tasks()

    if args.add:
        add_tasks(tasks, args.add)
    elif args.list:
        list_tasks(tasks)
    elif args.done:
        mark_done(tasks, args.done)
    elif args.delete:
        delete_task(tasks, args.delete)
    else:
        print("Please provide an action: --add, --list, --done, --delete, --clear")

    save_tasks(tasks)


if __name__ == "__main__":
    main()
