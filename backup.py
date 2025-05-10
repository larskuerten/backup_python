import os
import datetime
import zipfile


def crear_nombre_backup():
    """Generates a name for the backup file based at the current datetime"""
    fecha_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"backup_{fecha_hora}.zip"


def crear_backup(carpeta_origen, carpeta_destino):
    # Check if the folder do exist
    if not os.path.exists(carpeta_origen):
        print(f"Error: La carpeta de origen '{carpeta_origen}' no existe.")
        return None

    if not os.path.exists(carpeta_destino):
        print(f"Creando carpeta de destino '{carpeta_destino}' ...")
        os.makedirs(carpeta_destino)

    # Create backup filename
    nombre_backup = crear_nombre_backup()
    ruta_backup = os.path.join(carpeta_destino, nombre_backup)

    # Create ZIP file
    print(f"Creando backup en '{ruta_backup}'...")

    with zipfile.ZipFile(ruta_backup, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Loop thru source folder files
        for carpeta_actual, subcarpetas, archivos in os.walk(carpeta_origen):
            for archivo in archivos:
                ruta_archivo = os.path.join(carpeta_actual, archivo)
                # Store the ZIP file relative path
                ruta_relativa = os.path.relpath(
                    ruta_archivo, os.path.dirname(carpeta_origen)
                )
                zip_file.write(ruta_archivo, ruta_relativa)
                print(f"Añadido: {ruta_relativa}")

    print(f"Backup completado: {ruta_backup}")
    return ruta_backup


def main():
    """Función principal del programa"""
    print("=== BACKUP AUTOMATICO===")

    # Folder input
    carpeta_origen = input("Ingresa la ruta de la carpeta a respaldar: ")
    carpeta_destino = input(
        "Ingresa la ruta donde guardar el backup (deja en blanco para usar './backups'): "
    )

    if not carpeta_destino:
        carpeta_destino = "./backups"

    # Create backup
    ruta_backup = crear_backup(carpeta_origen, carpeta_destino)

    if ruta_backup:
        print(
            f"\nTamaño del backup: {os.path.getsize(ruta_backup) / (1024*1024):.2f} MB"
        )
        print("\nBackup completado con exito!")


if __name__ == "__main__":
    main()
