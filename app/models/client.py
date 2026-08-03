from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Cliente:
    nome: str
    telefone: str
    email: str
    id: Optional[int] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            nome=data["nome"],
            telefone=data["telefone"],
            email=data["email"],
        )
