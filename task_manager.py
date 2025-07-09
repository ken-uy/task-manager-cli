import argparse
import json
import os
import sys

# JSON file to store tasks
TASK_FILE = "tasks.json"


def load_tasks():
    # Load tasks from JSON file, return list
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    # Save tasks list to JSON file
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_tasks(tasks, description):
    # Find next id, append task, print confirmation
    new_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({"id": new_id, "task": description, "done": False})
    print(f"Added task [{new_id}]: {description}")


def list_tasks(tasks):
    # List all tasks with status
    if not tasks:
        print("No tasks")
    for t in tasks:
        status = "✅" if t["done"] else "❌"
        print(f"[{t['id']}]: {status} {t['task']}")


def mark_done(tasks, task_id):
    # Mark task as done by id
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            print("Task marked done")
            return
    print(f"[{task_id}] is not on the list")


def delete_tasks(tasks, delete_id):
    # Delete task by id
    for task in tasks:
        if task["id"] == delete_id:
            tasks.remove(task)
            print("Delete successful")
            return
    print(f"[{delete_id}] is not on the list")


def clear_tasks():
    # Clear all tasks from file
    with open(TASK_FILE, "w") as f:
        json.dump([], f, indent=2)
    print("Tasks cleared")


def main():
    # Parse CLI arguments
    parse = argparse.ArgumentParser()
    parse.add_argument("--add", type=str)
    parse.add_argument("--list", action="store_true")
    parse.add_argument("--done", type=int)
    parse.add_argument("--delete", type=int)
    parse.add_argument("--clear", action="store_true")
    args = parse.parse_args()

    if args.clear:
        # Clear tasks and exit
        clear_tasks()
        sys.exit(0)

    # Load existing tasks
    tasks = load_tasks()

    # Handle actions
    if args.add:
        add_tasks(tasks, args.add)
    elif args.list:
        list_tasks(tasks)
    elif args.done:
        mark_done(tasks, args.done)
    elif args.delete:
        delete_tasks(tasks, args.delete)
    else:
        print("Please use one of --add, --list, --done, --delete, or --clear")

    # Save updated tasks
    save_tasks(tasks)


if __name__ == "__main__":
    main()
