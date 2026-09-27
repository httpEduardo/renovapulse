"""Camada de dados e regras de prioridade do RenovaPulse."""
from __future__ import annotations
import sqlite3
from dataclasses import dataclass
from datetime import date
from pathlib import Path

@dataclass(frozen=True)
class Contract:
    id: int
    client: str
    monthly_value_cents: int
    renewal_date: date
    status: str
    @property
    def monthly_value(self) -> float:
        return self.monthly_value_cents / 100

class RenewalService:
    def __init__(self, database_path: str | Path = "renovapulse.db") -> None:
        self.database_path = str(database_path)
        self._initialize()
    def _connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection
    def _initialize(self) -> None:
        with self._connection() as connection:
            connection.execute("""CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client TEXT NOT NULL,
                monthly_value_cents INTEGER NOT NULL CHECK(monthly_value_cents > 0),
                renewal_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open', 'closed'))
            )""")
    def add_contract(self, client: str, monthly_value: float, renewal_date: date) -> Contract:
        if not client.strip(): raise ValueError("O nome do cliente é obrigatório.")
        cents = round(monthly_value * 100)
        if cents <= 0: raise ValueError("O valor mensal deve ser maior que zero.")
        with self._connection() as connection:
            cursor = connection.execute("INSERT INTO contracts (client, monthly_value_cents, renewal_date) VALUES (?, ?, ?)", (client.strip(), cents, renewal_date.isoformat()))
            identifier = cursor.lastrowid
        return self.get_contract(identifier)
    def get_contract(self, identifier: int) -> Contract:
        with self._connection() as connection:
            row = connection.execute("SELECT * FROM contracts WHERE id = ?", (identifier,)).fetchone()
        if row is None: raise ValueError(f"Contrato {identifier} não encontrado.")
        return self._to_contract(row)
    def list_open(self) -> list[Contract]:
        with self._connection() as connection:
            rows = connection.execute("SELECT * FROM contracts WHERE status = 'open' ORDER BY renewal_date, client").fetchall()
        return [self._to_contract(row) for row in rows]
    def upcoming(self, days: int, today: date | None = None) -> list[Contract]:
        if days < 0: raise ValueError("O período não pode ser negativo.")
        reference = today or date.today()
        return [item for item in self.list_open() if 0 <= (item.renewal_date - reference).days <= days]
    def renew(self, identifier: int, renewal_date: date) -> Contract:
        self.get_contract(identifier)
        with self._connection() as connection:
            connection.execute("UPDATE contracts SET renewal_date = ?, status = 'open' WHERE id = ?", (renewal_date.isoformat(), identifier))
        return self.get_contract(identifier)
    def close(self, identifier: int) -> Contract:
        self.get_contract(identifier)
        with self._connection() as connection:
            connection.execute("UPDATE contracts SET status = 'closed' WHERE id = ?", (identifier,))
        return self.get_contract(identifier)
    @staticmethod
    def priority(contract: Contract, today: date | None = None) -> str:
        remaining = (contract.renewal_date - (today or date.today())).days
        if remaining <= 7: return "CRÍTICA"
        if remaining <= 14: return "ALTA"
        if remaining <= 30: return "MÉDIA"
        return "PLANEJADA"
    @staticmethod
    def _to_contract(row: sqlite3.Row) -> Contract:
        return Contract(row["id"], row["client"], row["monthly_value_cents"], date.fromisoformat(row["renewal_date"]), row["status"])
