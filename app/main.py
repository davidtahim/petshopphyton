import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from app.services.pet_service import PetShopService


def load_routes():
    routes_file = Path(__file__).resolve().parent.parent / "data" / "rotas.json"
    with routes_file.open("r", encoding="utf-8") as file:
        return json.load(file)


ROUTINES = load_routes()


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
        print("\nNenhum cliente cadastrado.")
        return

    print("\n=== CLIENTES CADASTRADOS ===")
    for cliente in clientes:
        print(f"- ID {cliente.id}: {cliente.nome} | Telefone: {cliente.telefone} | Email: {cliente.email}")


def display_animais(animais):
    if not animais:
        print("\nNenhum animal cadastrado.")
        return

    print("\n=== ANIMAIS CADASTRADOS ===")
    for animal in animais:
        print(f"- ID {animal.id}: {animal.nome} | Espécie: {animal.especie} | Raça: {animal.raca} | Idade: {animal.idade} anos | Dono ID: {animal.dono_id}")


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

        try:
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

        except ValueError as exc:
            print(f"Erro de validação: {exc}")
        except Exception as exc:
            print(f"Erro inesperado: {exc}")


if __name__ == "__main__":
    main()
