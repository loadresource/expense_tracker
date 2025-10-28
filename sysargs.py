import argparse
import task_property


# Función para crear el parser de argumentos
# y definir los subcomandos
# Cada subcomando tiene su propio conjunto de argumentos
def create_parser():
    # Crear el parser
    arg_parser = argparse.ArgumentParser(description="Expense Tracker CLI")
   
    # Subcomando
    subparsers = arg_parser.add_subparsers(dest="command", help="Available commands")
   
    # Subcomando add
    parser_add = subparsers.add_parser("add", help="Add a new expense")
    parser_add.add_mutually_exclusive_group()
    parser_add.add_argument("--description", type=str, help="expense description")
    parser_add.add_argument("--amount", type=int, help="expense amount")
    parser_add.set_defaults(func=handle_add)
    
    # subcomando list
    parser_list = subparsers.add_parser("list", help="List tasks")
    group = parser_list.add_mutually_exclusive_group()
    group.add_argument("--todo", action="store_true", help="List todo tasks")
    group.add_argument("--done", action="store_true", help="List done tasks")
    group.add_argument("--in-progress", action="store_true", help="List in-progress tasks")
    parser_list.set_defaults(func=handle_list)
    
    #subcomando mark
    parser_mark = subparsers.add_parser("mark", help="Mark a task as done")
    parser_mark.add_argument("id", type=int, help="Task ID")
    parser_mark.add_argument("status", type=str, choices=["done", "todo", "in-progres"], help="New status (use 'inprogress' for 'in-progress', without dashes)")
    parser_mark.set_defaults(func=handle_mark)

    #subcomando update
    parser_update = subparsers.add_parser("update", help="Update a task's description")
    parser_update.add_argument("id", type=int, help="Task ID")  
    parser_update.add_argument("description", type=str, help="New task description")
    parser_update.set_defaults(func=handle_update)

    #subcomando delete
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("id", type=int, help="Task ID")
    parser_delete.set_defaults(func=handle_delete)

    return arg_parser
# Manejadores de subcomandos
# Cada manejador recibe los argumentos parseados
# y llama a la función correspondiente en task_property.py


# Manejador para el subcomando add
def handle_add(args):
    task, message = task_property.add(args.description,args.amount)
    print(message)
    print(task)


# Manejador para el subcomando list
def handle_list(args):
    status = None
    if args.todo:
        status = "todo"
    elif args.done:
        status = "done"
    elif args.in_progress:
        status = "in-progress"
    tasks = task_property.list(status)
    if tasks:
        for task in tasks:
            print(task)
    else:
        print("No tasks found.")


# Manejador para el subcomando mark
def handle_mark(args):
    message = task_property.mark(args.id, args.status)
    print(message)


# Manejador para el subcomando update
def handle_update(args):
    message = task_property.update(args.id, args.description)
    print(message)


# Manejador para el subcomando delete
def handle_delete(args):
    message = task_property.delete(args.id)
    print(message)