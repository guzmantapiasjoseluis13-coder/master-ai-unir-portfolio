"""Trabajo 1: Sintaxis Python - Calculadora de Promedios.

Curso de Programación en Python - UNIR (PER 17015)
Estudiante: Jose Luis Guzman Tapias
"""


def ingresar_calificaciones():
    """Permite al usuario ingresar materias y calificaciones (0-10).

    Retorna dos listas separadas: materias y calificaciones.
    """
    materias = []
    calificaciones = []

    print("\n--- Registro de Calificaciones Escolares ---")
    while True:
        materia = input("Ingrese el nombre de la materia: ").strip()
        if not materia:
            print("El nombre no puede estar vacío. Intente de nuevo.")
            continue

        while True:
            try:
                prompt_cal = f"Ingrese calificación para '{materia}' (0-10): "
                calificacion = float(input(prompt_cal))
                if 0 <= calificacion <= 10:
                    break
                else:
                    print("Error: La calificación debe ser entre 0 y 10.")
            except ValueError:
                print("Error: Por favor, ingrese un número válido.")

        materias.append(materia)
        calificaciones.append(calificacion)

        pregunta = "¿Desea ingresar otra materia? (s/n): "
        continuar = input(pregunta).strip().lower()
        if continuar != "s":
            break

    return materias, calificaciones


def calcular_promedio(calificaciones):
    """Calcula y devuelve el promedio general de calificaciones."""
    if not calificaciones:
        return 0.0
    return sum(calificaciones) / len(calificaciones)


def determinar_estado(calificaciones, umbral=5.0):
    """Devuelve índices de materias aprobadas y reprobadas según umbral."""
    aprobadas = []
    reprobadas = []
    for i, cal in enumerate(calificaciones):
        if cal >= umbral:
            aprobadas.append(i)
        else:
            reprobadas.append(i)
    return aprobadas, reprobadas


def encontrar_extremos(calificaciones):
    """Identifica el índice de la calificación máxima y mínima."""
    if not calificaciones:
        return None, None
    indice_max = calificaciones.index(max(calificaciones))
    indice_min = calificaciones.index(min(calificaciones))
    return indice_max, indice_min


def main():
    """Función principal que coordina el flujo del programa."""
    print("==================================================")
    print("   CALCULADORA DE PROMEDIOS ESCOLARES - UNIR      ")
    print("==================================================")

    materias, calificaciones = ingresar_calificaciones()

    if not materias:
        print("\n[Aviso] No se ingresó ninguna materia. ¡Hasta pronto!")
        return

    promedio_general = calcular_promedio(calificaciones)
    aprobadas_idx, reprobadas_idx = determinar_estado(
        calificaciones,
        umbral=5.0,
    )
    idx_max, idx_min = encontrar_extremos(calificaciones)

    print("\n" + "=" * 50)
    print("               RESUMEN ACADÉMICO FINAL              ")
    print("==================================================")

    print("\n📌 Listado Completo de Materias:")
    for m, c in zip(materias, calificaciones):
        estado = "Aprobada" if c >= 5.0 else "Reprobada"
        print(f"   - {m}: {c:.2f} ({estado})")

    print(f"\n📊 Promedio General: {promedio_general:.2f}")

    print("\n✅ Materias Aprobadas:")
    if aprobadas_idx:
        for i in aprobadas_idx:
            print(f"   - {materias[i]} ({calificaciones[i]:.2f})")
    else:
        print("   - Ninguna materia aprobada.")

    print("\n❌ Materias Reprobadas:")
    if reprobadas_idx:
        for i in reprobadas_idx:
            print(f"   - {materias[i]} ({calificaciones[i]:.2f})")
    else:
        print("   - Ninguna materia reprobada.")

    if idx_max is not None and idx_min is not None:
        mat_max, val_max = materias[idx_max], calificaciones[idx_max]
        mat_min, val_min = materias[idx_min], calificaciones[idx_min]
        print(f"\n🏆 Mejor Calificación: {mat_max} con {val_max:.2f}")
        print(f"⚠️ Peor Calificación: {mat_min} con {val_min:.2f}")

    print("\n" + "=" * 50)
    print("¡Gracias por utilizar el sistema! ¡Hasta pronto!")
    print("==================================================")


if __name__ == "__main__":
    main()
