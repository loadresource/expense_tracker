# Expense Tracker CLI

Small command-line Expense Tracker used in the roadmap.sh project.[challenge](https://roadmap.sh/projects/expense-tracker)

## Features
- Add, list, update and delete expenses.
- Simple JSON-backed storage (table-like structure: headers + rows).
- Export JSON -> CSV.

## Requirements
- Python 3.8+
- (optional) a virtual environment for isolation
## Installation
1. Clone the repository:
    git clone <repository-url>
2. (Recommended) Create and activate a virtual environment:
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install dependencies if any (project currently uses stdlib only):
    pip install -r requirements.txt # if you add dependencies later
## Usage
Run the main script with Python, followed by the desired command and options. For example:
    python main.py add --description "Lunch" --amount 12.50
    python main.py list
    python main.py update --id 1 --amount 15.00
    python main.py delete --id 1
    python main.py summary
    python main.py export -i name.json --output name.csv
## Commands
- Add an expense
- List expenses
- Update an expense
- Delete an expense
- Summary (project defines a `summary` subcommand; follow the CLI help if its arguments differ)
- Convert JSON storage to CSV
or call the helper directly:
    python -m source.json_to_csv -i data.json -o data.csv
## Data file format (data.json)
The storage is a small "table" JSON with this shape:
```json
{
  "headers": ["id","description","amount","status","createdAt","updateAt"],
  "rows": [
    [0, "Lunch", 12, "todo", "2025-10-30", "2025-10-30 12:00:00"],
    ...
  ]
}
```
## License
This project is licensed under the MIT License. See the LICENSE file for details.
## Contributing
Contributions are welcome! Please open issues or pull requests for improvements or bug fixes.