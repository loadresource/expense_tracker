import argparse
import handlers as hd


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
    parser_add.set_defaults(func=hd.handle_add)

    # subcomando list
    parser_list = subparsers.add_parser("list", help="List expense")
    group = parser_list.add_mutually_exclusive_group()
    group.add_argument("--todo", action="store_true", help="List todo tasks")
    parser_list.set_defaults(func=hd.handle_list)

    # subcomando update
    parser_update = subparsers.add_parser("update", help="Update a expense's description")
    parser_update.add_argument("--id", type=int, help="Task ID")
    parser_update.add_argument("--description", type=str, help="New expense description")
    parser_update.add_argument("--amount", type=int, help="New mount")
    parser_update.set_defaults(func=hd.handle_update)

    # subcomando delete
    parser_delete = subparsers.add_parser("delete", help="Delete a expense")
    parser_delete.add_argument("id", type=int, help="Task ID")
    parser_delete.set_defaults(func=hd.handle_delete)

    #subcomando summary amount
    parser_sum = subparsers.add_parser("summary", help="total amount")
    parser_sum.add_argument("total",help="Total summary expense")
    parser_sum.set_defaults(func=hd.handle_sumatori)


    return arg_parser