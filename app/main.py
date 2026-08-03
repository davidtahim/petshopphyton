import sys
from pathlib import Path

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from app.services.pet_service import PetShopService


ROUTINES = {
    "2": {
        "label": "Listar clientes",
        "entity": "cliente",
        "method": "listar_clientes",
        "action": "list",
    },
    "3": {
        "label": "Buscar cliente",
        "entity": "cliente",
        "method": "buscar_cliente",
        "action": "get",
    },
    "4": {
        "label": "Atualizar cliente",
        "entity": "cliente",
        "method": "atualizar_cliente",
        "action": "update",
    },
    "5": {
        "label": "Excluir cliente",
        "entity": "cliente",
        "method": "excluir_cliente",
        "action": "delete",
    },
    "6": {
        "label": "Cadastrar animal",
        "entity": "animal",
        "method": "cadastrar_animal",
        "action": "create",
    },
    "7": {
        "label": "Listar animais",
        "entity": "animal",
        "method": "listar_animais",
        "action": "list",
    },
    "8": {
        "label": "Buscar animal",
        "entity": "animal",
        "method": "buscar_animal",
        "action": "get",
    },
    "9": {
        "label": "Atualizar animal",
        "entity": "animal",
        "method": "atualizar_animal",
        "action": "update",
    },
    "10": {
        "label": "Excluir animal",
        "entity": "animal",
        "method": "excluir_animal",
        "action": "delete",
    },
}


def build_menu() -> str:
    lines = [
        "+====================================+",
        "|          PET SHOP SYSTEM           |",
        "+====================================+",
        "| 1. Cadastrar cliente               |",
    ]

    for code, item in ROUTINES.items():
        label = item["label"]
        padding = 35 - len(label)
        lines.append(f"| {code}. {label}{' ' * padding}|")

    lines.extend([
        "| 0. Sair                            |",
        "+====================================+",
    ])
    return "\n".join(lines)


def display_clientes(clientes):
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return

    print("\nClientes:")
    for cliente in clientes:
        print(f"- ID {cliente.id}: {cliente.nome} | {cliente.telefone} | {cliente.email}")


def display_animais(animais):
    if not animais:
        print("Nenhum animal cadastrado.")
        return

    print("\nAnimais:")
    for animal in animais:
        print(f"- ID {animal.id}: {animal.nome} | {animal.especie} | {animal.raca} | {animal.idade} anos | dono_id={animal.dono_id}")


def handle_choice(service: PetShopService, option: str, data=None):
    data = data or []

    if option == "1":
        nome, telefone, email = data
        return service.cadastrar_cliente(nome, telefone, email)

    if option in ROUTINES:
        method_name = ROUTINES[option]["method"]
        method = getattr(service, method_name)

        if ROUTINES[option]["action"] == "list":
            return method()

        if ROUTINES[option]["action"] == "get":
            entity_id = int(data[0])
            return method(entity_id)

        if ROUTINES[option]["action"] == "delete":
            entity_id = int(data[0])
            return method(entity_id)

        if ROUTINES[option]["action"] == "update":
            if ROUTINES[option]["entity"] == "cliente":
                cliente_id, nome, telefone, email = data
                return method(int(cliente_id), nome, telefone, email)
            animal_id, nome, especie, raca, idade, dono_id = data
            return method(int(animal_id), nome, especie, raca, int(idade), int(dono_id))

        if ROUTINES[option]["action"] == "create":
            nome, especie, raca, idade, dono_id = data
            return method(nome, especie, raca, int(idade), int(dono_id))

    return None


def main() -> None:
    service = PetShopService()
    print("Sistema Pet Shop inicializado.")

    while True:
        print(build_menu())
        option = input("Escolha uma opção: ").strip()

        if option == "0":
            print("Saindo do sistema...")
            break

        if option == "1":
            nome = input("Nome: ").strip()
            telefone = input("Telefone: ").strip()
            email = input("Email: ").strip()
            cliente = handle_choice(service, option, [nome, telefone, email])
            print("Cliente cadastrado:", cliente)

        elif option == "2":
            clientes = handle_choice(service, option)
            display_clientes(clientes)

        elif option == "3":
            cliente_id = input("ID do cliente: ").strip()
            cliente = handle_choice(service, option, [cliente_id])
            print("Cliente encontrado:", cliente)

        elif option == "4":
            cliente_id = input("ID do cliente: ").strip()
            nome = input("Novo nome: ").strip()
            telefone = input("Novo telefone: ").strip()
            email = input("Novo email: ").strip()
            cliente = handle_choice(service, option, [cliente_id, nome, telefone, email])
            print("Cliente atualizado:", cliente)

        elif option == "5":
            cliente_id = input("ID do cliente: ").strip()
            removido = handle_choice(service, option, [cliente_id])
            print("Cliente removido:", removido)

        elif option == "6":
            nome = input("Nome do animal: ").strip()
            especie = input("Espécie: ").strip()
            raca = input("Raça: ").strip()
            idade = input("Idade: ").strip()
            dono_id = input("ID do dono: ").strip()
            animal = handle_choice(service, option, [nome, especie, raca, idade, dono_id])
            print("Animal cadastrado:", animal)

        elif option == "7":
            animais = handle_choice(service, option)
            display_animais(animais)

        elif option == "8":
            animal_id = input("ID do animal: ").strip()
            animal = handle_choice(service, option, [animal_id])
            print("Animal encontrado:", animal)

        elif option == "9":
            animal_id = input("ID do animal: ").strip()
            nome = input("Novo nome: ").strip()
            especie = input("Nova espécie: ").strip()
            raca = input("Nova raça: ").strip()
            idade = input("Nova idade: ").strip()
            dono_id = input("Novo ID do dono: ").strip()
            animal = handle_choice(service, option, [animal_id, nome, especie, raca, idade, dono_id])
            print("Animal atualizado:", animal)

        elif option == "10":
            animal_id = input("ID do animal: ").strip()
            removido = handle_choice(service, option, [animal_id])
            print("Animal removido:", removido)

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
