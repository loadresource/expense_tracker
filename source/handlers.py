import source.expense_property as expense_property
import source.json_to_csv as json_to_csv
# Manejadores de subcomandos
# Cada manejador recibe los argumentos parseados
# y llama a la función correspondiente en task_property.py

# Manejador para el subcomando add
def handle_add(args):
    task, message = expense_property.add(args.description, args.amount)
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

    tasks = expense_property.list(status)
    if tasks:
        print(f"|{"ID":^4} | {"Description":^20} | {"Amount":^10} | {"Date":^12}")
        for task in tasks:
            print(
                f"""  
|{task.get("id"):^4} | {task.get("description"):^20} | {task.get("amount"):^10} | {task.get("updateAt"):^12}"""
            )
    else:
        print("Expense not found.")


# Manejador para el subcomando update
def handle_update(args):
    message = expense_property.update(args.id, args.description,args.amount)
    print(message)


# Manejador para el subcomando delete
def handle_delete(args):
    message = expense_property.delete(args.id)
    print(message)


def handle_sumatori(args):
    summ = expense_property.sum_amounts()
    print(f"total :{summ}")

def handle_converter_csv(args):
    json_to_csv.json_to_csv(args.input_file, args.output_file)
