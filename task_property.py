
from datetime import datetime, date
import json
import os

class Task:
    def __init__(self, ID, description,amount, status, createdAt, updateAt):
        self.ID = ID
        self.description = description
        self.amount = amount
        self.status = status
        self.createdAt = createdAt
        self.updateAt = updateAt
    
    def __getitem__(self, key):
        # Para mantener compatibilidad con el código existente
        return getattr(self, key)


#generar explicacion
class GeneradorID:
    _instancia = None
    _id_actual = -1  # Valor por defecto
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GeneradorID, cls).__new__(cls)
            # Al crear la instancia, cargar el último ID desde el archivo
            cls._cargar_ultimo_id()
        return cls._instancia
    
    def siguiente(self):
        GeneradorID._id_actual += 1
        # Guardar el nuevo ID actual en el archivo
        self._guardar_ultimo_id()
        return GeneradorID._id_actual
    
    @classmethod
    def _cargar_ultimo_id(cls):
        """Carga el último ID desde el archivo data.json"""
        try:
            if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
                with open("data.json", "r") as file:
                    data = json.load(file)
                    if data:  # Si hay datos en el archivo
                        # Encontrar el ID más alto en los datos existentes
                        max_id = max(item["id"] for item in data)
                        cls._id_actual = max_id
        except (json.JSONDecodeError, FileNotFoundError, ValueError):
            # Si hay algún error, comenzar desde -1
            cls._id_actual = -1
    
    @classmethod
    def _guardar_ultimo_id(cls):
        """Guarda el último ID en un archivo separado para persistencia"""
        try:
            with open("last_id.json", "w") as file:
                json.dump({"last_id": cls._id_actual}, file)
        except IOError:
            print("Error al guardar el último ID")
    
generador_id = GeneradorID()

def obj_to_json(task):
    return {
        "id": task["ID"],
        "description": task["description"],
        "amount": task["amount"],
        "status": task["status"],
        "createdAt": task["createdAt"].strftime("%Y-%m-%d"),
        "updateAt": task["updateAt"].strftime("%Y-%m-%d %H:%M:%S")
    }


def add(description: str,amount: int):
    # Usar la instancia compartida del generador de IDs
    task = Task(
        ID = generador_id.siguiente(),
        description = description,
        amount = amount,
        status = "todo",
        createdAt = date.today(),
        updateAt = datetime.now()
    )
    save(task)
    return task, f"expense added successfully ID({task.ID})"

def save(task):
    """
    Agrega una nueva tarea al archivo data.json sin reescribir el contenido existente.
    
    Args:
        task: Objeto de tarea a guardar
    """
    filename = "data.json"
    
    try:
        # Leer tareas existentes o inicializar lista vacía
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, "r") as file:
                try:
                    tasks = json.load(file)
                except json.JSONDecodeError:
                    tasks = []
        else:
            tasks = []
        
        # Convertir la tarea a formato JSON y agregarla a la lista
        task_json = obj_to_json(task)
        tasks.append(task_json)
        
        # Escribir todas las tareas de vuelta al archivo
        with open(filename, "w") as file:
            json.dump(tasks, file, indent=2)
            
    except IOError as e:
        print(f"Error al guardar la tarea: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")


def update(id: int, description: str):
    if os.path.exists("data.json"):
        with open("data.json", "r") as data:
            tasks = json.load(data)
        found = False
        for task in tasks:
            if task["id"] == id:
                task["description"] = description
                task["updateAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                found = True
                break
        if found:
            with open("data.json", "w") as data:
                json.dump(tasks, data, indent=2)
            return f"Task {id} updated successfully"
    return f"Task {id} not found"

def mark(id: int, status: str):
    if os.path.exists("data.json"):
        with open("data.json", "r") as data:
            tasks = json.load(data)
        found = False
        for task in tasks:
            if task["id"] == id:
                task["status"] = status
                task["updateAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                found = True
                break
        if found:
            with open("data.json", "w") as data:
                json.dump(tasks, data, indent=2)
            return f"Task {id} marked as {status} successfully"
    return f"Task {id} not found"

def list(status=None):
    """
    Lista las tareas filtrando por el estado si se proporciona.

    Args:
        status (str, optional): Puede ser "__done", "__todo" o "__in-progress". Si es None, retorna todas las tareas.

    Returns:
        list: Lista de tareas filtradas o todas si status es None.
    """
    if os.path.exists("data.json"):
        with open("data.json", "r") as data:
            tasks = json.load(data)
            if status in ("done", "todo", "in-progres"):
                tasks = [task for task in tasks if task["status"] == status]
            return tasks
    return None


def delete(task_id):
    if os.path.exists("data.json"):
        with open("data.json", "r") as data:
            tasks = json.load(data)
            tasks = [t for t in tasks if t["id"] != task_id]
        with open("data.json", "w") as data:
            json.dump(tasks, data, indent=2)
    return f"Task {task_id} deleted successfully"