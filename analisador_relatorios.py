"""Analisa um arquivo CSV de atividades e gera um relatório de produtividade."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Atividade:
    responsavel: str
    categoria: str
    horas: float
    status: str


def carregar_atividades(caminho: str | Path) -> list[Atividade]:
    atividades: list[Atividade] = []
    with Path(caminho).open(encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        obrigatorias = {"responsavel", "categoria", "horas", "status"}
        if not leitor.fieldnames or not obrigatorias.issubset(leitor.fieldnames):
            raise ValueError(f"O CSV deve conter as colunas: {sorted(obrigatorias)}")
        for linha in leitor:
            atividades.append(
                Atividade(
                    responsavel=linha["responsavel"].strip(),
                    categoria=linha["categoria"].strip(),
                    horas=float(linha["horas"].replace(",", ".")),
                    status=linha["status"].strip().lower(),
                )
            )
    return atividades


def analisar(atividades: list[Atividade]) -> dict:
    horas_por_pessoa: dict[str, float] = defaultdict(float)
    horas_por_categoria: dict[str, float] = defaultdict(float)
    status = Counter()

    for atividade in atividades:
        horas_por_pessoa[atividade.responsavel] += atividade.horas
        horas_por_categoria[atividade.categoria] += atividade.horas
        status[atividade.status] += 1

    total = len(atividades)
    concluidas = status.get("concluida", 0) + status.get("concluído", 0)
    taxa = (concluidas / total * 100) if total else 0.0
    return {
        "total_atividades": total,
        "total_horas": round(sum(a.horas for a in atividades), 2),
        "taxa_conclusao": round(taxa, 1),
        "horas_por_pessoa": dict(sorted(horas_por_pessoa.items())),
        "horas_por_categoria": dict(sorted(horas_por_categoria.items())),
        "status": dict(sorted(status.items())),
    }


def gerar_relatorio(resultado: dict) -> str:
    linhas = [
        "RELATÓRIO DE PRODUTIVIDADE",
        "=" * 30,
        f"Atividades: {resultado['total_atividades']}",
        f"Horas registradas: {resultado['total_horas']:.2f}",
        f"Taxa de conclusão: {resultado['taxa_conclusao']:.1f}%",
        "",
        "Horas por pessoa:",
    ]
    linhas.extend(
        f"- {nome}: {horas:.2f} h"
        for nome, horas in resultado["horas_por_pessoa"].items()
    )
    linhas.append("")
    linhas.append("Horas por categoria:")
    linhas.extend(
        f"- {categoria}: {horas:.2f} h"
        for categoria, horas in resultado["horas_por_categoria"].items()
    )
    return "\n".join(linhas) + "\n"


def executar() -> None:
    parser = argparse.ArgumentParser(description="Analisador de relatórios CSV")
    parser.add_argument("arquivo_csv")
    parser.add_argument("--saida", default="relatorio_produtividade.txt")
    args = parser.parse_args()

    resultado = analisar(carregar_atividades(args.arquivo_csv))
    relatorio = gerar_relatorio(resultado)
    Path(args.saida).write_text(relatorio, encoding="utf-8")
    print(relatorio)
    print(f"Relatório salvo em {args.saida}")


if __name__ == "__main__":
    executar()
