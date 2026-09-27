"""Interface de linha de comando do RenovaPulse."""
from __future__ import annotations
import argparse
from datetime import date
from .service import RenewalService

def parse_date(value: str) -> date:
    try: return date.fromisoformat(value)
    except ValueError as error: raise argparse.ArgumentTypeError("Use AAAA-MM-DD.") from error

def money(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main() -> None:
    parser = argparse.ArgumentParser(description="Acompanhe renovações e MRR em risco.")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add"); add.add_argument("--cliente", required=True); add.add_argument("--valor", required=True, type=float); add.add_argument("--vence", required=True, type=parse_date)
    commands.add_parser("list")
    dashboard = commands.add_parser("dashboard"); dashboard.add_argument("--dias", default=30, type=int)
    renew = commands.add_parser("renew"); renew.add_argument("id", type=int); renew.add_argument("--vence", required=True, type=parse_date)
    close = commands.add_parser("close"); close.add_argument("id", type=int)
    args = parser.parse_args(); service = RenewalService()
    try:
        if args.command == "add": print(f"Contrato #{service.add_contract(args.cliente,args.valor,args.vence).id} cadastrado.")
        elif args.command == "list":
            for c in service.list_open(): print(f"#{c.id} | {c.client} | {money(c.monthly_value)} | vence {c.renewal_date} | {service.priority(c)}")
        elif args.command == "dashboard":
            contracts = service.upcoming(args.dias); print(f"MRR em risco: {money(sum(c.monthly_value for c in contracts))}")
            for c in contracts: print(f"#{c.id} | {c.client} | vence {c.renewal_date} | {service.priority(c)}")
        elif args.command == "renew": print(f"Contrato #{service.renew(args.id,args.vence).id} renovado.")
        else: print(f"Contrato #{service.close(args.id).id} encerrado.")
    except ValueError as error: raise SystemExit(f"Erro: {error}") from error
if __name__ == "__main__": main()
