from tp1 import *

tb1 = table({'a': (1,1)}, nb=2)
tb2 = table({'b': (2,2)}, nb=2)
for tp in produit_cartesien(tb1,tb2):
    print(tp)