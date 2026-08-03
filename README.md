# Pet Shop Python

Projeto base para um sistema CRUD de pet shop em Python, organizado por camadas para facilitar manutenção e extensão.

## Estrutura

- `app/` - lógica da aplicação
  - `models/` - entidades do domínio
  - `repositories/` - acesso a dados
  - `services/` - regras de negócio
  - `utils/` - utilitários
- `data/` - arquivos de persistência
- `tests/` - testes automatizados

## Como executar

```bash
python3 run.py
```

## Como testar

```bash
pytest
```

## Funcionalidades previstas

- Cadastro de clientes
- Cadastro de animais
- Listagem, edição e remoção
- Persistência em JSON
- Estrutura pronta para expansão com banco de dados e interface web
