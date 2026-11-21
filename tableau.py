from code_base_EP1 import *

class FormulaMarcada:
   def __init__ (self, sinal, formula):
      # valida se o sinal é valido
      if sinal not in ("T", "F"):
         raise ValueError("Sinal inválido")

      # guarda os valores dentro do objeto
      self.sinal = sinal
      self.formula = formula
  
   def __str__ (self):
      # f-string: funcionacomo um print(objeto)
      return f"{self.sinal} {self.formula}"

   def eh_igual (self, outra):
      # compara objetos
      cmp = self.sinal == outra.sinal and self.formula.is_identical(outra.formula)

      return cmp

# teste
# P, Q, R = vars("P", "Q", "R")

# f1 = FormulaMarcada("T", P)
# f2 = FormulaMarcada("T", ~~P)
# f3 = FormulaMarcada("T", P)

# print("f1 == f2: ", f1.eh_igual(f2))
# print("f1 == f3: ", f1.eh_igual(f3))
# print("f1: ", f1)
# print("f2: ", f2)

class Ramo:
  def __init__ (self):
    self.nao_expandidas = []
    self.expandidas = []
    self.atomos = {}
    self.fechado = False

  def adicionar (self, fm):
    if (self.fechado): return
    valor = (fm.sinal == "T")

    # caso 1 fm.formula é uma constante (True ou False)
    if isinstance(fm.formula, Constant):
      contradicao = fm.formula.value != valor

      if (contradicao): self.fechado = True
    
    # caso 2 - fm.formula é uma variable (atomo)
    elif isinstance(fm.formula, Variable):
      nome = fm.formula.name

      if nome in self.atomos:
        if (self.atomos[nome] != valor): self.fechado = True

      else: self.atomos[nome] = valor
        
    # caso 3 - formula composta (~, and, or, =>)
    else:
      ja_existe_formula = False
      for formula in self.nao_expandidas + self.expandidas:
        if (formula.eh_igual(fm)): ja_existe_formula = True

      if not ja_existe_formula:
        self.nao_expandidas.append(fm)

  def clonar(self):
    novo_ramo = Ramo()
    novo_ramo.atomos = self.atomos.copy()
    novo_ramo.expandidas = self.expandidas.copy()
    novo_ramo.nao_expandidas = self.nao_expandidas.copy()
    novo_ramo.fechado = self.fechado

    return novo_ramo

  def esta_saturada(self):
    if (not self.fechado and len(self.nao_expandidas) == 0): return True

    return False

# test
# P, Q, R = vars("P", "Q", "R")

# r = Ramo()

# f1 = FormulaMarcada("T", P)
# f2 = FormulaMarcada("T", P >> Q)

# r.adicionar(f1)
# r.adicionar(f2)

# r_esq = r.clonar()
# r_dir = r.clonar()

# f_esq = FormulaMarcada("F", P)
# r_esq.adicionar(f_esq)

# f_dir = FormulaMarcada("T", Q)
# r_dir.adicionar(f_dir)

# print(r_esq.fechado, r_dir.fechado, r_dir.atomos)


