"""Primer programa del curso: un saludo con una clase."""


class Saludo:
    """Representa un saludo dirigido a una persona."""

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre

    def texto(self) -> str:
        return f"Hola, {self.nombre}. Bienvenido al módulo 5100."


if __name__ == "__main__":
    saludo = Saludo("mundo")
    print(saludo.texto())
