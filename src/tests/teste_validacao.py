import unittest
from utils.validacao import validar_proposicao_entrada

class TesteValidacao(unittest.TestCase):
    def test_proposicoes_diferente_de_vazio(self):
        self.assertIsNotNone(validar_proposicao_entrada("p >> q, r & s"))
 
    def test_parenteses_c(self):
        resultado = validar_proposicao_entrada(' (p >> q) , (((a | b) >> q) & (∼s))')
        self.assertEqual(resultado, ['(p>>q)', '(((a|b)>>q)&(∼s))'], f'{resultado}')

    def test_proposicao_atomo(self):
        self.assertEqual(validar_proposicao_entrada("p"), ['p'])

    #TESTES DE ERRO-------------------------------------------------------------
    def test_proposicoes_none(self):
        with self.assertRaises(ValueError):
            validar_proposicao_entrada("")

    def test_proposicoes_vazias(self):
        with self.assertRaises(ValueError):
            validar_proposicao_entrada("p >> q, , r & s")

    def test_proposicao_vazia(self):
        with self.assertRaises(ValueError):
            validar_proposicao_entrada("p >> q, ")

    def test_parenteses_incompletos(self):
        with self.assertRaises(ValueError):
            validar_proposicao_entrada("(p >> q")

    def test_proposicao_somente_operador(self):
        with self.assertRaises(ValueError):
            validar_proposicao_entrada(">>")