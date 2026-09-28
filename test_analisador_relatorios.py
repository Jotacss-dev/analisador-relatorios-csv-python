import unittest

from analisador_relatorios import Atividade, analisar, gerar_relatorio


class TestAnalisador(unittest.TestCase):
    def test_calcula_indicadores(self):
        atividades = [
            Atividade("Jailton", "Pesquisa", 2.0, "concluida"),
            Atividade("Jailton", "Dados", 3.0, "pendente"),
        ]
        resultado = analisar(atividades)
        self.assertEqual(resultado["total_atividades"], 2)
        self.assertEqual(resultado["total_horas"], 5.0)
        self.assertEqual(resultado["taxa_conclusao"], 50.0)
        self.assertIn("RELATÓRIO DE PRODUTIVIDADE", gerar_relatorio(resultado))


if __name__ == "__main__":
    unittest.main()
