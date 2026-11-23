# Curso de especialización en Desarrollo de aplicaciones en lenguaje Python

- **Alumno/a:** Daniel Valencia Hernández
- **Usuario GitHub:** dvh793
- **Centro:** CIFP César Manrique

## 5100 · Programación orientada a objetos

| Carpeta | Unidad de trabajo |
|---------|-------------------|
| 5100/UT0 | Puesta en marcha y repaso de Python |
| 5100/UT1 | Fundamentos de la POO |
| 5100/UT2 | Clases avanzadas y organización del código |
| 5100/UT3 | Persistencia en ficheros y serialización |
| 5100/UT4 | Bases de datos y aplicaciones web |
| 5100/UT5 | Proyecto intermodular (pruebas y documentación) |

## 5101 · Análisis de datos con Python

| Carpeta | Unidad de trabajo |
|---------|-------------------|
| 5101/UT0 | Puesta en marcha y repaso de Python |
| 5101/UT1 | Carga, exportación y persistencia de datos |
| 5101/UT2 | Limpieza, normalización y estandarización de datos |
| 5101/UT3 | Análisis exploratorio y visualización |
| 5101/UT4 | Modelado y predicción |
| 5101/UT5 | Proyecto intermodular |

```mermaid
classDiagram
    direction LR
    class GestorClientes {
        -clientes: dict~str, Cliente~
        +alta(nombre: str, correo: str, nif: str) Cliente
        +baja(correo: str) bool
        +buscar(correo: str) Cliente
        +buscar_por_nif(nif: str) Cliente
        +estadisticas() dict
        +__len__() int
    }
    class Cliente {
        +IGIC: float = 0.07$
        +nombre: str
        +correo: str
        +nif: str
        +registrar_pedido(p: Pedido) None
        +añadir_contacto(c: Contacto) None
        +gasto_total() float
        +categoria() str
        +es_nif_valido(nif: str)$ bool
        +__str__() str
    }
    class Pedido {
        +importe: float
        +concepto: str
        +pagado: bool = False
        +total_con_igic() float
        +__str__() str
    }
    class Contacto {
        +nombre: str
        +telefono: str
        +cargo: str
        +__str__() str
    }
    GestorClientes "1" *-- "0..*" Cliente : clientes
    Cliente "1" *-- "0..*" Pedido : pedidos
    Cliente "1" o-- "0..*" Contacto : contactos
```
