import re

from app.models.animal import Animal
from app.models.client import Cliente
from app.repositories.json_repository import JsonRepository


class PetShopService:
    def __init__(self, clients_path="data/clientes.json", animals_path="data/animais.json"):
        self.clientes = JsonRepository(clients_path, Cliente)
        self.animais = JsonRepository(animals_path, Animal)

    @staticmethod
    def validar_email(email: str) -> None:
        padrao = r"^[\w\.-]+@([\w-]+\.)+[a-zA-Z]{2,}$"
        if not re.match(padrao, email):
            raise ValueError("Email inválido")

    @staticmethod
    def validar_telefone(telefone: str) -> None:
        if len(telefone) < 10:
            raise ValueError("Telefone inválido")

    @staticmethod
    def validar_idade(idade: int) -> None:
        if idade < 0:
            raise ValueError("Idade inválida")

    def cadastrar_cliente(self, nome: str, telefone: str, email: str):
        nome = nome.strip()
        telefone = telefone.strip()
        email = email.strip()

        if not nome:
            raise ValueError("Nome obrigatório")
        self.validar_telefone(telefone)
        self.validar_email(email)

        cliente = Cliente(nome=nome, telefone=telefone, email=email)
        cliente.id = self._next_id(self.clientes.data)
        return self.clientes.add(cliente)

    def listar_clientes(self):
        return self.clientes.list_all()

    def buscar_cliente(self, cliente_id: int):
        return self.clientes.get_by_id(cliente_id)

    def atualizar_cliente(self, cliente_id: int, nome: str, telefone: str, email: str):
        nome = nome.strip()
        telefone = telefone.strip()
        email = email.strip()

        if not nome:
            raise ValueError("Nome obrigatório")
        self.validar_telefone(telefone)
        self.validar_email(email)

        cliente = Cliente(id=cliente_id, nome=nome, telefone=telefone, email=email)
        return self.clientes.update(cliente_id, cliente)

    def excluir_cliente(self, cliente_id: int):
        return self.clientes.delete(cliente_id)

    def cadastrar_animal(self, nome: str, especie: str, raca: str, idade: int, dono_id: int):
        nome = nome.strip()
        especie = especie.strip()
        raca = raca.strip()

        if not nome or not especie or not raca:
            raise ValueError("Nome, espécie e raça são obrigatórios")
        self.validar_idade(idade)

        animal = Animal(nome=nome, especie=especie, raca=raca, idade=idade, dono_id=dono_id)
        animal.id = self._next_id(self.animais.data)
        return self.animais.add(animal)

    def listar_animais(self):
        return self.animais.list_all()

    def buscar_animal(self, animal_id: int):
        return self.animais.get_by_id(animal_id)

    def atualizar_animal(self, animal_id: int, nome: str, especie: str, raca: str, idade: int, dono_id: int):
        nome = nome.strip()
        especie = especie.strip()
        raca = raca.strip()

        if not nome or not especie or not raca:
            raise ValueError("Nome, espécie e raça são obrigatórios")
        self.validar_idade(idade)

        animal = Animal(id=animal_id, nome=nome, especie=especie, raca=raca, idade=idade, dono_id=dono_id)
        return self.animais.update(animal_id, animal)

    def excluir_animal(self, animal_id: int):
        return self.animais.delete(animal_id)

    @staticmethod
    def _next_id(data):
        if not data:
            return 1
        return max(item.get("id", 0) for item in data) + 1
