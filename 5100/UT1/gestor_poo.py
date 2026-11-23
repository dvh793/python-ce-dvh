"""Gestor de clientes con clases (UT1): refactorización de gestor_v0.py."""


class Pedido:
    """Un pedido de un cliente."""

    def __init__(self, importe, concepto="varios"):
        if not isinstance(importe, (int, float)) or importe <= 0:
            raise ValueError(f"Importe no válido: {importe!r}")
        self.importe = float(importe)
        self.concepto = concepto.strip() or "varios"

    def __str__(self):
        return f"{self.concepto}: {self.importe:.2f} €"

    def __repr__(self):
        return f"Pedido({self.importe!r}, {self.concepto!r})"


class Cliente:
    """Un cliente de Alisios Renovables y sus pedidos."""

    IGIC = 0.07

    def __init__(self, nombre, correo):
        nombre = nombre.strip().title()
        correo = correo.strip().lower()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        if not Cliente.es_correo_valido(correo):
            raise ValueError(f"Correo no válido: {correo!r}")
        self.nombre = nombre
        self.correo = correo
        self.pedidos = []

    @staticmethod
    def es_correo_valido(correo):
        """Un @, usuario no vacío y un punto en el dominio."""
        if correo.count("@") != 1:
            return False
        usuario, dominio = correo.split("@")
        return bool(usuario) and "." in dominio

    @classmethod
    def desde_linea(cls, linea):
        """'Nombre;correo;importe;importe...' -> Cliente con sus pedidos."""
        nombre, correo, *importes = linea.split(";")
        cliente = cls(nombre, correo)
        for importe in importes:
            cliente.registrar_pedido(Pedido(float(importe)))
        return cliente

    def registrar_pedido(self, pedido):
        self.pedidos.append(pedido)

    def gasto_total(self):
        return round(sum(p.importe for p in self.pedidos) * (1 + Cliente.IGIC), 2)

    def categoria(self):
        gasto = self.gasto_total()
        if gasto >= 1000:
            return "oro"
        if gasto >= 500:
            return "plata"
        return "bronce"

    def __len__(self):
        return len(self.pedidos)

    def __str__(self):
        return (
            f"{self.nombre:<20} {self.correo:<25} {len(self):>3} pedidos "
            f"{self.gasto_total():>10.2f} € {self.categoria()}"
        )

    def __repr__(self):
        return f"Cliente({self.nombre!r}, {self.correo!r})"


class GestorClientes:
    """La colección de clientes: alta, baja, búsqueda y listado."""

    def __init__(self):
        self._clientes = {}  # correo -> Cliente

    def alta(self, nombre, correo):
        cliente = Cliente(nombre, correo)  # valida (o lanza ValueError)
        if cliente.correo in self._clientes:
            raise ValueError(f"Ya existe un cliente con el correo {cliente.correo}")
        self._clientes[cliente.correo] = cliente
        return cliente

    def baja(self, correo):
        return self._clientes.pop(correo.strip().lower(), None) is not None

    def buscar(self, correo):
        return self._clientes.get(correo.strip().lower())

    def listar(self):
        return sorted(self._clientes.values(), key=lambda c: c.nombre)

    def __len__(self):
        return len(self._clientes)


def menu():
    gestor = GestorClientes()
    while True:
        print("\n1) Alta  2) Pedido  3) Listar  4) Baja  0) Salir")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                gestor.alta(input("Nombre: "), input("Correo: "))
                print("Alta correcta.")
            elif opcion == "2":
                cliente = gestor.buscar(input("Correo: "))
                if cliente is None:
                    print("Cliente no encontrado.")
                else:
                    importe = float(input("Importe: "))
                    cliente.registrar_pedido(Pedido(importe, input("Concepto: ")))
                    print("Pedido registrado.")
            elif opcion == "3":
                if len(gestor) == 0:
                    print("No hay clientes.")
                for cliente in gestor.listar():
                    print(cliente)
            elif opcion == "4":
                if gestor.baja(input("Correo: ")):
                    print("Baja realizada.")
                else:
                    print("No existe.")
            elif opcion == "0":
                break
            else:
                print("Opción no válida.")
        except ValueError as err:
            print("Error:", err)


if __name__ == "__main__":
    menu()
