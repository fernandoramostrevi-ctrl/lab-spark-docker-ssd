import json
from datetime import datetime

# Autor: Juan Gutierrez Miranda
# Fecha de creación: 2024-01-27

class Ingrediente:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def get_nombre(self):
        return self.nombre

    def get_precio(self):
        return self.precio

class Sandwich:
    def __init__(self):
        self.ingredientes = []
        self.total = 0.0

    def agregar_ingrediente(self, ingrediente):
        self.ingredientes.append(ingrediente)
        self.total += ingrediente.get_precio()

    def get_ingredientes(self):
        return self.ingredientes

    def get_total(self):
        return self.total

class Compra:
    def __init__(self, sandwich):
        self.id = self._get_ultimo_id() + 1
        self.timestamp = self._obtener_timestamp()
        self.sandwich = sandwich

    def get_id(self):
        return self.id

    def get_timestamp(self):
        return self.timestamp

    def get_sandwich(self):
        return self.sandwich

    def guardar_compra(self):
        compra_data = {
            "id": self.id,
            "timestamp": self.timestamp,
            "ingredients": [ingrediente.get_nombre() for ingrediente in self.sandwich.get_ingredientes()],
            "total": self.sandwich.get_total()
        }

        try:
            with open("purchases.json", "r") as f:
                compras = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            compras = []

        compras.append(compra_data)

        with open("purchases.json", "w") as f:
            json.dump(compras, f, indent=4)

    def _get_ultimo_id(self):
        try:
            with open("purchases.json", "r") as f:
                compras = json.load(f)
            return compras[-1]["id"]
        except (FileNotFoundError, IndexError, json.JSONDecodeError):
            return 0

    def _obtener_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class SistemaCompras:
    def __init__(self):
        self.ingredientes = {
            "lechuga": Ingrediente("lechuga", 10),
            "tomate": Ingrediente("tomate", 15),
            "queso": Ingrediente("queso", 20),
            "jamón": Ingrediente("jamón", 30),
            "pollo": Ingrediente("pollo", 40),
            "pan": Ingrediente("pan", 50)
        }
        self.compras = self._obtener_compras()

    def _obtener_compras(self):
        try:
            with open("purchases.json", "r") as f:
                compras_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        compras = []
        for compra_data in compras_data:
            sandwich = Sandwich()
            for ingrediente_nombre in compra_data["ingredients"]:
                sandwich.agregar_ingrediente(self.ingredientes[ingrediente_nombre.lower()])
            compra = Compra(sandwich)
            compra.id = compra_data["id"]
            compra.timestamp = compra_data["timestamp"]
            compras.append(compra)

        return compras