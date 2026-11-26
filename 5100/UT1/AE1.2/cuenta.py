class CuentaBancaria:
    """Cuenta bancaria sencilla con historial de movimientos."""
    numero_cuentas = 0
    COMISION_DESCUBIERTO = 5.0

    def __init__(self, titular, saldo_inicial=0.0):
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo")
        self.titular = titular
        self.saldo = float(saldo_inicial)
        self.movimientos = []
        CuentaBancaria.numero_cuentas += 1

    def ingresar(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        self.saldo += cantidad
        self.movimientos.append(("ingreso", cantidad))

    def retirar(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        if cantidad > self.saldo:
            raise ValueError("Saldo insuficiente")
        self.saldo -= cantidad
        self.movimientos.append(("retirada", cantidad))

    @classmethod
    def desde_texto(cls, texto):
        titular, saldo = texto.split(":")
        return cls(titular.strip(), float(saldo))

    @staticmethod
    def iban_valido(iban):
        return len(iban) == 24 and iban[:2].isalpha() and iban[2:].isdigit()

    def __len__(self):
        return len(self.movimientos)

    def __str__(self):
        return f"{self.titular}: {self.saldo:.2f} € ({len(self)} movimientos)"

    def __del__(self):
        print(f"Cuenta de {self.titular} cerrada")