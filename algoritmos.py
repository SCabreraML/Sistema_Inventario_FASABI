
class BubbleSort:
    def ordenar(self, lista, clave):
        n = len(lista)
        for i in range(n):
            for j in range(0, n - i - 1):
                if lista[j][clave] > lista[j + 1][clave]:
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]
        return lista


class QuickSort:
    def ordenar(self, lista, clave):
        if len(lista) <= 1:
            return lista
        pivot = lista[0][clave]
        menor = [x for x in lista[1:] if x[clave] <= pivot]
        mayor = [x for x in lista[1:] if x[clave] > pivot]
        return self.ordenar(menor, clave) + [lista[0]] + self.ordenar(mayor, clave)


class BinarySearch:
    def buscar(self, lista, clave, valor):
        inicio = 0
        fin = len(lista) - 1
        while inicio <= fin:
            medio = (inicio + fin) // 2
            if lista[medio][clave] == valor:
                return lista[medio]
            elif lista[medio][clave] < valor:
                inicio = medio + 1
            else:
                fin = medio - 1
        return None
