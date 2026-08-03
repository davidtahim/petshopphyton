from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Animal:
    nome: str
    especie: str
    raca: str
    idade: int
    dono_id: int
    id: Optional[int] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            nome=data["nome"],
            especie=data["especie"],
            raca=data["raca"],
            idade=data["idade"],
            dono_id=data["dono_id"],
        )
