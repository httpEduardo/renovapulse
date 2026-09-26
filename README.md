# RenovaPulse

RenovaPulse é um MVP de linha de comando para consultores, agências e pequenos B2B que vendem contratos recorrentes. Ele registra clientes, calcula a receita mensal recorrente (MRR) em risco e lista quais renovações devem receber atenção primeiro.

## Proposta

Perder uma renovação por esquecimento custa mais do que a maioria das pequenas equipes consegue medir. O RenovaPulse centraliza a carteira em um banco SQLite local, transforma datas de término em prioridades e entrega uma visão objetiva da receita que vence nos próximos dias.

O produto pode começar como ferramenta local para validar o fluxo e evoluir para um SaaS multiusuário com alertas por e-mail/WhatsApp, importação de CRM e painéis para gestores.

## Requisitos

- Python 3.11 ou superior
- Nenhuma dependência externa

## Instalação

```bash
git clone <URL_DO_REPOSITORIO>
cd renovapulse
python -m venv .venv
```

Ative o ambiente virtual se desejar; o projeto usa apenas a biblioteca padrão do Python.

## Uso

Os dados ficam em `renovapulse.db` no diretório corrente. Execute usando `python -m renovapulse`:

```bash
python -m renovapulse add --cliente "Ateliê Aurora" --valor 1500 --vence 2026-10-15
python -m renovapulse list
python -m renovapulse dashboard --dias 30
python -m renovapulse renew 1 --vence 2027-10-15
python -m renovapulse close 1
```

O campo `--valor` aceita ponto decimal (por exemplo, `1500.50`). A prioridade é calculada por prazo: crítica (até 7 dias), alta (até 14), média (até 30) e planejada (acima disso).

## Testes

```bash
python -m unittest discover -s tests -v
```

## Modelo de receita

- **Grátis:** até 25 contratos e painel local.
- **Solo (R$ 29/mês):** alertas, histórico de contatos e exportação CSV.
- **Equipe (R$ 99/mês):** usuários ilimitados, permissões, CRM e alertas colaborativos.
- **Receita adicional:** implantação/importação de carteira para agências e consultorias.

O MVP atual privilegia validação: mede se pessoas conseguem cadastrar a carteira e agir sobre os contratos críticos. A próxima versão comercial pode hospedar o banco, adicionar autenticação e cobrar por conta de equipe.

## Privacidade e segurança

Não há tokens, senhas nem chaves embutidos. O banco local contém dados de negócio; não o envie a repositórios públicos. O arquivo `renovapulse.db` está ignorado pelo Git.

## Licença

MIT. Consulte [LICENSE](LICENSE).
