# tipos básicos


# str

# int

# float

# lista

# dict

# tuple

tupla = (2, 3, 4, 5)
# tupla[0] = 44, vai dar error, tupla não aceita atribuição


def hello_world(name="Wagner"):
    print("hello_world {}".format(name))


name = input("Digite seu nome: \n")
if name:
    hello_world(name)


for i in range(0, 20):
    print(i)


lista = ["sdadas", 2, [2, 3, 4]]

for i in lista:
    print(i)


nova_lista = []


for i in lista:
    if i != 2:
        nova_lista.append(i)


import ipdb

ipdb.set_trace()  # breakpoint f911e1e6 //


nova_lista = [i for i in lista if i != 2]
