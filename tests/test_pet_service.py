from app.services.pet_service import PetShopService


def test_cadastrar_e_listar_clientes():
    service = PetShopService(clients_path="data/test_clientes.json", animals_path="data/test_animais.json")

    cliente = service.cadastrar_cliente("Maria", "11999999999", "maria@email.com")

    assert cliente["nome"] == "Maria"
    assert cliente["id"] == 1
    assert len(service.listar_clientes()) == 1


def test_cadastrar_e_listar_animais():
    service = PetShopService(clients_path="data/test_clientes.json", animals_path="data/test_animais.json")

    service.cadastrar_cliente("João", "11888888888", "joao@email.com")
    animal = service.cadastrar_animal("Rex", "Cachorro", "Vira-lata", 3, 1)

    assert animal["nome"] == "Rex"
    assert animal["dono_id"] == 1
    assert len(service.listar_animais()) == 1
