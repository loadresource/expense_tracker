from datetime import datetime, date
import json
import os


class Expense:
    def __init__(self, ID, description, amount, status, createdAt, updateAt):
        self.ID = ID
        self.description = description
        self.amount = amount
        self.status = status
        self.createdAt = createdAt
        self.updateAt = updateAt

    def __getitem__(self, key):
        # Para mantener compatibilidad con el código existente
        return getattr(self, key)


# generar explicacion
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
        """Carga el último ID desde el archivo data.json en formato tabla"""
        try:
            if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
                with open("data.json", "r") as file:
                    data = json.load(file)
                    
                    # Verificar que tenga la estructura de tabla esperada
                    if isinstance(data, dict) and "rows" in data and "headers" in data:
                        rows = data["rows"]
                        if rows:
                            # El ID está en la primera columna (posición 0) de cada fila
                            ids = [fila[0] for fila in rows if fila and len(fila) > 0]
                            if ids:
                                cls._id_actual = max(ids)
                            else:
                                cls._id_actual = -1
                        else:
                            # No hay filas, empezar desde -1
                            cls._id_actual = -1
                    else:
                        # No es el formato esperado, tratar como archivo vacío
                        print("Advertencia: Formato de archivo no reconocido. Se reiniciarán los IDs.")
                        cls._id_actual = -1
            else:
                # Archivo no existe o está vacío
                cls._id_actual = -1
                
        except (json.JSONDecodeError, FileNotFoundError, ValueError, KeyError, IndexError) as e:
            # Si hay algún error, comenzar desde -1
            print(f"Error al cargar último ID: {e}")
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


def add(description: str, amount: int):
    # Usar la instancia compartida del generador de IDs
    task = Expense(
        ID=generador_id.siguiente(),
        description=description,
        amount=amount,
        status="todo",
        createdAt=date.today(),
        updateAt=datetime.now(),
    )
    save(task)
    return task, f"expense added successfully ID({task.ID})"


def save(task):
    """
    Agrega una nueva tarea al archivo data.json en formato de tabla
    sin reescribir el contenido existente.

    Args:
        task: Objeto de tarea a guardar
    """
    filename = "data.json"

    try:
        # Leer datos existentes o inicializar estructura de tabla
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, "r") as file:
                try:
                    table_data = json.load(file)
                except json.JSONDecodeError:
                    table_data = create_table_structure()
        else:
            table_data = create_table_structure()

        # Convertir la tarea a formato de tabla y agregarla
        task_row = obj_to_table_row(task)
        add_row_to_table(table_data, task_row)

        # Escribir la tabla de vuelta al archivo
        with open(filename, "w") as file:
            json.dump(table_data, file, indent=2)

    except IOError as e:
        print(f"Error al guardar la tarea: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")


def create_table_structure():
    """Crea la estructura inicial de la tabla"""
    return {
        "headers": ["id", "description", "amount", "status", "createdAt", "updateAt"],
        "rows": []
    }


def obj_to_table_row(header):
    """Convierte un objeto task en una fila de la tabla"""
    return [
        header["ID"],
        header["description"],
        header["amount"],
        header["status"],
        header["createdAt"].strftime("%Y-%m-%d"),
        header["updateAt"].strftime("%Y-%m-%d %H:%M:%S")
    ]


def add_row_to_table(table_data, task_row):
    """Agrega una fila a la estructura de tabla"""
    table_data["rows"].append(task_row)


def update(id: int, description: str, amount: int):
    """
    Actualiza una tarea en el archivo data.json basado en el ID proporcionado.

    Args:
        id (int): ID de la tarea a actualizar
        description (str): Nueva descripción de la tarea
        amount (int): Nuevo monto de la tarea

    Returns:
        str: Mensaje indicando el resultado de la operación
    """
    if not os.path.exists("data.json"):
        return "Error: No se encontró el archivo data.json"

    try:
        with open("data.json", "r") as data:
            table_data = json.load(data)
        
        # Verificar que tenga la estructura de tabla esperada
        if not isinstance(table_data, dict) or "headers" not in table_data or "rows" not in table_data:
            return "Error: Formato de archivo no válido"
        
        headers = table_data["headers"]
        rows = table_data["rows"]
        
        # Encontrar los índices de las columnas que necesitamos
        try:
            id_index = headers.index("id")
            description_index = headers.index("description")
            amount_index = headers.index("amount")
            updateAt_index = headers.index("updateAt")
        except ValueError as e:
            return f"Error: Columna no encontrada en los headers: {e}"
        
        # Buscar y actualizar la tarea
        found = False
        for row in rows:
            if row[id_index] == id:
                # Actualizar los campos
                row[description_index] = description
                row[amount_index] = amount
                row[updateAt_index] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                found = True
                break
        
        if found:
            # Escribir los datos actualizados de vuelta al archivo
            with open("data.json", "w") as data:
                json.dump(table_data, data, indent=2)
            return f"Task {id} updated successfully"
        else:
            return f"Task {id} not found"
            
    except (json.JSONDecodeError, IOError) as e:
        return f"Error al procesar el archivo: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

def list(status=None):
    """
    Obtiene todas las tareas del archivo data.json en formato de tabla.
    
    Args:
        status (str, optional): Filtra las tareas por estado. Si es None, devuelve todas.
    
    Returns:
        list or None: Lista de tareas en formato de diccionario o None si no hay datos
    """
    if os.path.exists("data.json"):
        try:
            with open("data.json", "r") as data:
                table_data = json.load(data)
                
                # Verificar que tenga la estructura de tabla esperada
                if isinstance(table_data, dict) and "headers" in table_data and "rows" in table_data:
                    headers = table_data["headers"]
                    rows = table_data["rows"]
                    
                    # Convertir filas a diccionarios usando los headers como claves
                    tasks = []
                    for row in rows:
                        if len(row) == len(headers):
                            task_dict = dict(zip(headers, row))
                            
                            # Aplicar filtro por status si se especificó
                            if status is None or task_dict.get("status") == status:
                                tasks.append(task_dict)
                    return tasks
                
                else:
                    print("Advertencia: Formato de archivo no reconocido")
                    return None
                    
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al leer el archivo: {e}")
            return None
    
    return None


def delete(task_id):
    """
    Elimina una tarea del archivo data.json basado en el ID proporcionado.

    Args:
        task_id: ID de la tarea a eliminar

    Returns:
        str: Mensaje indicando el resultado de la operación
    """
    if not os.path.exists("data.json"):
        return "Error: No se encontró el archivo data.json"

    try:
        with open("data.json", "r") as data:
            table_data = json.load(data)
            
        # Verificar que tenga la estructura de tabla esperada
        if not isinstance(table_data, dict) or "headers" not in table_data or "rows" not in table_data:
            return "Error: Formato de archivo no válido"
        
        # Filtrar las filas, excluyendo la que tiene el ID a eliminar
        original_count = len(table_data["rows"])
        table_data["rows"] = [row for row in table_data["rows"] if row and row[0] != task_id]
        new_count = len(table_data["rows"])
        
        # Escribir los datos actualizados de vuelta al archivo
        with open("data.json", "w") as data:
            json.dump(table_data, data, indent=2)
        
        if new_count < original_count:
            return f"Task {task_id} deleted successfully"
        else:
            return f"Task {task_id} not found"
            
    except (json.JSONDecodeError, IOError) as e:
        return f"Error al procesar el archivo: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"


def sum_amounts():
    """
    Versión simple que suma todos los amounts sin filtrar por estado.
    """
    try:
        if not os.path.exists("data.json"):
            return 0.0
            
        with open("data.json", "r") as file:
            table_data = json.load(file)
        
        if not isinstance(table_data, dict) or "headers" not in table_data or "rows" not in table_data:
            return 0.0
        
        headers = table_data["headers"]
        rows = table_data["rows"]
        
        amount_index = headers.index("amount")
        
        total = 0.0
        for row in rows:
            if len(row) > amount_index:
                try:
                    total += float(row[amount_index])
                except (ValueError, TypeError):
                    continue
        
        return total
        
    except Exception:
        return 0.0
