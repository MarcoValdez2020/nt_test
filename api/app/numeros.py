
class Numeros:
    """Clase para representar el conjunto de los primeros 100 números"""

    def __init__(self):
        """Inicializa la lista de números"""
        self.numeros = list(range(1, 101))


    def extraer_numero(self, numero: int):
        """Extrae un número de la lista
        Args:
            numero (int): El número a extraer
        Raises:
            TypeError: Si el número no es un entero
            ValueError: Si el número no está entre 1 y 100
            ValueError: Si ya se ha extraído un número
        Returns:
            str: Mensaje de éxito
        """
        print(len(self.numeros))
        if not isinstance(numero, int):
            raise TypeError("El número debe ser un entero")
        if numero < 1 or numero > 100:
            raise ValueError("El número debe estar entre 1 y 100")
        if len(self.numeros) < 100:
            raise ValueError("Solo se puede extraer un número")
        
        
        self.numeros.remove(numero)
        return f'Número extraído correctamente: {numero}'
    

    def calcular_numero_extraido(self):
        """Calcula el número extraído
        Returns:
            int: El número extraído
        Raises:
            ValueError: Si no se ha extraído ningún número
        """
        if len(self.numeros) == 100:
            raise ValueError("No se ha extraído ningún número")
        
        # Genero una lista completa y obtengo el número extraído
        lista_completa = list(range(1, 101))
        # Transformo la lista a un set, y obtengo la diferencia que es el número extraído
        numero_extraido = set(lista_completa) - set(self.numeros)

        return numero_extraido.pop()


    def reiniciar(self):
        """Reinicia la lista de números"""
        self.numeros = list(range(1, 101))
        return "Lista reiniciada correctamente"

