"""La BIBLIOTECA del centro tiene SOCIOS y EJEMPLARES. Cada EJEMPLAR pertenece a un TITULO (con ISBN y autor) y puede estar disponible o prestado. Un SOCIO puede tener hasta tres PRESTAMOS; un PRESTAMO relaciona un EJEMPLAR con un SOCIO y tiene fecha de inicio y fecha de devolución prevista. La BIBLIOTECA *da de alta* SOCIOS, *presta* EJEMPLARES y *registra* DEVOLUCIONES."""

```mermaid
classDiagram
	direction LR
	class Biblioteca{
		-socios: dict~str, Socio~
		-ejemplares dict~str, Ejemplar~
		+alta_socio(nombre: str, correo: str, nif: str) Socio
		+nuevo_prestamo()
		+devolucion()

	}
	class Socio{
		+nombre: str
        +correo: str
        +nif: str
		+prestamos: dict~str, Prestamo~
	}
	class Prestamo{
		+ejemplar
		+socio
		+f_inicio
		+f_fin
	}
	class Ejemplar{
		+titulo dict~str, Titulo~
		+disponible
	}
	class Titulo{
		+isbn
		+autor
	}
	Biblioteca "1" *-- "0..*" Socio : socios
	Biblioteca "1" *-- "0..*" Ejemplar : ejemplares
	Socio "1" *-- "0..3*" Prestamo : prestamos
