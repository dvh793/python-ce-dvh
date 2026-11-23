class Pedido:
    IGIC = 0.07

    def __init__(self,importe,concepto="varios"):
        self.importe = importe
        self.concepto = concepto
    #def cerrar_y_facturar_e_imprimir(self, enviar_email=False):
    # marca el pedido como pagado, calcula el total con IGIC, lo imprime
    # y, si enviar_email es True, imprime "enviando factura"

#Pedido->pagado
#total + igic
#Mostrar
#Si esta marcado enviar_email -> mostrar aviso

    def pagar(self):
        self.pagado = True
    def total(self):
        return self.importe + (self.importe * self.IGIC)
    def factura(self):
        return f"{self.concepto}: {self.total()} "

p = Pedido(100,"papas")
p.pagar()
print(p.total())
print(p.factura())