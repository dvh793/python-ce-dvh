"""Gestor de clientes de Alisios Renovables, S.L. — versión 0 (programación estructurada).

Punto de partida del módulo 5100: diccionarios y funciones, sin clases.
En la UT 1 lo refactorizaremos a objetos; antes, léelo con atención y fíjate en:
  - agenda es una variable global que todas las funciones leen y modifican;
  - la forma de cada registro ({"nombre": ..., "pedidos": [...]}) se repite en varias funciones;
  - nada impide que otra parte del programa rompa esa forma;
  - las validaciones (correo, importe) hay que acordarse de llamarlas.
"""

IGIC = 0.07  # impuesto aplicado al gasto total

# correo -> {"nombre": str, "pedidos": [importes]}
agenda: dict[str, dict] = {}


def es_correo_valido(correo: str) -> bool:
    """Un @, usuario no vacío y un punto en el dominio."""
    if correo.count("@") != 1:
        return False
    usuario, dominio = correo.split("@")
    return bool(usuario) and "." in dominio


def alta(nombre: str, correo: str) -> bool:
    """Da de alta un cliente. Devuelve False si el correo no es válido o ya existe."""
    nombre = nombre.strip().title()
    correo = correo.strip().lower()
    if not nombre or not es_correo_valido(correo) or correo in agenda:
        return False
    agenda[correo] = {"nombre": nombre, "pedidos": []}
    return True


def baja(correo: str) -> bool:
    """Elimina un cliente. Devuelve False si no existe."""
    return agenda.pop(correo.strip().lower(), None) is not None


def buscar(correo: str) -> dict | None:
    """Devuelve el registro del cliente o None."""
    return agenda.get(correo.strip().lower())


def registrar_pedido(correo: str, importe: float) -> bool:
    """Añade un pedido al cliente. Devuelve False si no existe o el importe no es válido."""
    cliente = buscar(correo)
    if cliente is None or importe <= 0:
        return False
    cliente["pedidos"].append(float(importe))
    return True


def gasto_total(correo: str) -> float:
    """Suma de los pedidos del cliente con IGIC, redondeada a céntimos."""
    cliente = buscar(correo)
    if cliente is None:
        return 0.0
    return round(sum(cliente["pedidos"]) * (1 + IGIC), 2)


def pedido_mayor(correo: str) -> float:
    """Importe del mayor pedido (0 si no hay pedidos)."""
    cliente = buscar(correo)
    if cliente is None or not cliente["pedidos"]:
        return 0.0
    return max(cliente["pedidos"])


def categoria(gasto: float) -> str:
    """oro >= 1000, plata >= 500, bronce el resto."""
    if gasto >= 1000:
        return "oro"
    if gasto >= 500:
        return "plata"
    return "bronce"


def listar() -> None:
    """Imprime todos los clientes ordenados por gasto, de mayor a menor."""
    if not agenda:
        print("  (sin clientes)")
        return
    correos = sorted(agenda, key=gasto_total, reverse=True)
    for correo in correos:
        cliente = agenda[correo]
        gasto = gasto_total(correo)
        print(f"  {cliente['nombre']:<20} {correo:<25} {len(cliente['pedidos']):>3} pedidos "
              f"{gasto:>10.2f} €  {categoria(gasto)}")


def cargar_datos_de_ejemplo() -> None:
    """Unos clientes para no empezar con la agenda vacía."""
    alta("Ana Pérez", "ana@correo.es")
    registrar_pedido("ana@correo.es", 120.0)
    registrar_pedido("ana@correo.es", 80.5)
    alta("Hotel Teide Mar", "compras@teidemar.es")
    registrar_pedido("compras@teidemar.es", 950.0)
    registrar_pedido("compras@teidemar.es", 310.0)
    alta("Bodegas Tacoronte", "info@bodegastacoronte.es")


def pedir_importe() -> float:
    """Pide un importe hasta que sea un número positivo."""
    while True:
        try:
            importe = float(input("  Importe (€): ").replace(",", "."))
            if importe > 0:
                return importe
        except ValueError:
            pass
        print("  Importe no válido.")


def menu() -> None:
    opciones = {"1": "Alta de cliente", "2": "Baja de cliente", "3": "Registrar pedido",
                "4": "Consultar cliente", "5": "Listar clientes", "0": "Salir"}
    while True:
        print("\nGESTOR DE CLIENTES · Alisios Renovables")
        for clave, texto in opciones.items():
            print(f"  {clave}. {texto}")
        opcion = input("Opción: ").strip()
        if opcion == "0":
            print("Hasta luego.")
            break
        if opcion == "1":
            nombre = input("  Nombre: ")
            correo = input("  Correo: ")
            print("  Alta correcta." if alta(nombre, correo) else "  No se pudo dar de alta (correo no válido o repetido).")
        elif opcion == "2":
            print("  Baja correcta." if baja(input("  Correo: ")) else "  No existe ese cliente.")
        elif opcion == "3":
            correo = input("  Correo: ")
            if buscar(correo) is None:
                print("  No existe ese cliente.")
            else:
                registrar_pedido(correo, pedir_importe())
                print("  Pedido registrado.")
        elif opcion == "4":
            correo = input("  Correo: ")
            cliente = buscar(correo)
            if cliente is None:
                print("  No existe ese cliente.")
            else:
                gasto = gasto_total(correo)
                print(f"  {cliente['nombre']} · {len(cliente['pedidos'])} pedidos · "
                      f"gasto {gasto:.2f} € (mayor: {pedido_mayor(correo):.2f} €) · {categoria(gasto)}")
        elif opcion == "5":
            listar()
        else:
            print("  Opción no válida.")


if __name__ == "__main__":
    cargar_datos_de_ejemplo()
    menu()
