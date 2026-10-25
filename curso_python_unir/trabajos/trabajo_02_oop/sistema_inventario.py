class Producto:

    def __init__(self, nombre: str, precio: float, cantidad: int):
        """Constructor de la clase Producto."""
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValueError("El precio debe ser >= 0.")
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad debe ser >= 0.")

        self.nombre = nombre.strip()
        self.precio = float(precio)
        self.cantidad = int(cantidad)

    def actualizar_precio(self, nuevo_precio: float):
        """Actualiza el precio del producto."""
        if not isinstance(nuevo_precio, (int, float)) or nuevo_precio < 0:
            raise ValueError("El precio nuevo debe ser >= 0.")
        self.precio = float(nuevo_precio)

    def actualizar_cantidad(self, nueva_cantidad: int):
        """Actualiza la cantidad del producto."""
        if not isinstance(nueva_cantidad, int) or nueva_cantidad < 0:
            raise ValueError("La cantidad nueva debe ser >= 0.")
        self.cantidad = int(nueva_cantidad)

    def calcular_valor_total(self) -> float:
        """Calcula el valor total del producto."""
        return self.precio * self.cantidad

    def __str__(self) -> str:
        """Devuelve representación en cadena."""
        p = self.precio
        c = self.cantidad
        t = self.calcular_valor_total()
        return (
            f"Producto: {self.nombre} | "
            f"Precio: ${p:.2f} | "
            f"Cantidad: {c} | "
            f"Total: ${t:.2f}"
        )


class Inventario:

    def __init__(self):
        """Inicializa inventario vacío."""
        self.productos = []

    def agregar_producto(self, producto: Producto):
        """Agrega un producto a la lista."""
        if not isinstance(producto, Producto):
            raise TypeError("Debe ser instancia de Producto.")
        self.productos.append(producto)

    def buscar_producto(self, nombre: str):
        """Busca producto por nombre exacto."""
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("Nombre de búsqueda vacío.")
        nb = nombre.strip().lower()
        for prod in self.productos:
            if prod.nombre.lower() == nb:
                return prod
        return None

    def calcular_valor_inventario(self) -> float:
        """Calcula el valor total del inventario."""
        return sum(p.calcular_valor_total() for p in self.productos)

    def listar_productos(self):
        """Muestra todos los productos."""
        if not self.productos:
            print("\nInventario vacío.")
        else:
            print("\n--- LISTADO DE PRODUCTOS ---")
            for i, p in enumerate(self.productos, start=1):
                print(f"{i}. {p}")
            print("-" * 30)


def menu_principal():
    """Ejecuta el menú interactivo."""
    inv = Inventario()

    while True:
        print("\n=== MENÚ INVENTARIO ===")
        print("1. Agregar producto")
        print("2. Buscar producto")
        print("3. Listar productos")
        print("4. Calcular valor total")
        print("5. Salir")

        try:
            op = input("Seleccione opción (1-5): ").strip()

            if op == "1":
                print("\n--- Nuevo Producto ---")
                nom = input("Nombre: ")
                pre_str = input("Precio: ")
                can_str = input("Cantidad: ")
                pre = float(pre_str)
                can = int(can_str)
                prod = Producto(nom, pre, can)
                inv.agregar_producto(prod)
                print(f"¡Éxito! '{prod.nombre}' agregado.")

            elif op == "2":
                print("\n--- Buscar Producto ---")
                nom = input("Nombre a buscar: ")
                res = inv.buscar_producto(nom)
                if res:
                    print(f"\nEncontrado: {res}")
                else:
                    print(f"\nNo existe '{nom}'.")

            elif op == "3":
                inv.listar_productos()

            elif op == "4":
                tot = inv.calcular_valor_inventario()
                print(f"\nValor total: ${tot:.2f}")

            elif op == "5":
                print("\nSaliendo del sistema...")
                break
            else:
                print("\nOpción inválida (1-5).")

        except ValueError as ve:
            print(f"\nError de valor: {ve}")
        except Exception as e:
            print(f"\nError inesperado: {e}")


if __name__ == "__main__":
    menu_principal()
