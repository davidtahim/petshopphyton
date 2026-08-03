import pytest

from app.services.pet_service import PetShopService


def test_validar_cliente_rejeita_email_invalido(tmp_path):
    service = PetShopService(
        clients_path=str(tmp_path / "clientes.json"),
        animals_path=str(tmp_path / "animais.json"),
    )

    with pytest.raises(ValueError, match="Email inválido"):
        service.cadastrar_cliente("Maria", "11999999999", "email_invalido")


def test_validar_animal_rejeita_idade_negativa(tmp_path):
    service = PetShopService(
        clients_path=str(tmp_path / "clientes.json"),
        animals_path=str(tmp_path / "animais.json"),
    )

    with pytest.raises(ValueError, match="Idade inválida"):
        service.cadastrar_animal("Rex", "Cachorro", "Vira-lata", -1, 1)
