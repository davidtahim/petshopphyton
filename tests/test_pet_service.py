from app.services.pet_service import PetShopService


def test_cadastrar_e_listar_clientes(tmp_path):
    clientes_path = tmp_path / "test_clientes.json"
    animais_path = tmp_path / "test_animais.json"
    service = PetShopService(clients_path=str(clientes_path), animals_path=str(animais_path))

    cliente = service.cadastrar_cliente("Maria", "11999999999", "maria@email.com")

    assert cliente["nome"] == "Maria"
    assert cliente["id"] == 1
    assert len(service.listar_clientes()) == 1


def test_cadastrar_e_listar_animais(tmp_path):
    clientes_path = tmp_path / "test_clientes.json"
    animais_path = tmp_path / "test_animais.json"
    service = PetShopService(clients_path=str(clientes_path), animals_path=str(animais_path))

    service.cadastrar_cliente("João", "11888888888", "joao@email.com")
    animal = service.cadastrar_animal("Rex", "Cachorro", "Vira-lata", 3, 1)

    assert animal["nome"] == "Rex"
    assert animal["dono_id"] == 1
    assert len(service.listar_animais()) == 1
