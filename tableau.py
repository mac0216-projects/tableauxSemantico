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

# fórmulas
# todos os átomos que serão utilizados nas fórmulas precisam ser declarados
P, Q, R = vars("P", "Q", "R")

f1 = FormulaMarcada("T", P)
f2 = FormulaMarcada("T", ~~P)
f3 = FormulaMarcada("T", P)

formula1 = (P >> (Q >> R)| (Q >> (P|R)))

f4 = FormulaMarcada("T", formula1)

print(f1)
print(f2)
print(f4)


print("f1 == f2: ", f1.eh_igual(f2))
print("f1 == f3: ", f1.eh_igual(f3))

