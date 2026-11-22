import unittest
from utils.parser import parsear_proposicoes

class ParserTest(unittest.TestCase):
    def test_proposicoes_diferente_de_vazio(self):
        self.assertIsNotNone(parsear_proposicoes("p >> q, r & s"))

    def test_parenteses_c(self):
        resultado = parsear_proposicoes(' (p >> q) , (((a | b) >> q) & (∼s))')
        self.assertEqual(resultado, ['(p>>q)', '(((a|b)>>q)&(∼s))'], f'{resultado}')

    def test_proposicao_atomo(self):
        self.assertEqual(parsear_proposicoes("p"), ['p'])

    #TESTES DE ERRO-------------------------------------------------------------
    def test_proposicoes_none(self):
        with self.assertRaises(ValueError):
            parsear_proposicoes("")

    def test_proposicoes_vazias(self):
        with self.assertRaises(ValueError):
            parsear_proposicoes("p >> q, , r & s")

    def test_proposicao_vazia(self):
        with self.assertRaises(ValueError):
            parsear_proposicoes("p >> q, ")

    def test_parenteses_incompletos(self):
        with self.assertRaises(ValueError):
            parsear_proposicoes("(p >> q")

    def test_proposicao_somente_operador(self):
        with self.assertRaises(ValueError):
            parsear_proposicoes(">>")

    def test_operador_binario_com_um_atomo(self):
        with self.assertRaises(ValueError):
            parsear_proposicoes("p>>")