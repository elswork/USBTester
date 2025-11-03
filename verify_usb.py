
import os
import sys
import time

def get_drive_letter():
    """Solicita al usuario la letra de la unidad USB."""
    while True:
        drive = input("Introduce la letra de la unidad USB a verificar (ej. E): ").strip().upper()
        if len(drive) == 1 and 'A' <= drive <= 'Z':
            return f"{drive}:\\"
        else:
            print("Entrada inválida. Por favor, introduce solo una letra.")

def confirm_destruction(drive_path):
    """Muestra una advertencia y pide confirmación para borrar los datos."""
    print("\n" + "="*50)
    print("¡ADVERTENCIA MUY IMPORTANTE!")
    print("="*50)
    print(f"El siguiente proceso borrará TODOS los datos en la unidad '{drive_path}'.")
    print("Este proceso es IRREVERSIBLE.")
    print("Asegúrate de haber hecho una copia de seguridad de cualquier dato valioso.")
    print("="*50 + "\n")
    
    confirm = input(f"Escribe 'BORRAR' para confirmar y empezar la verificación en '{drive_path}': ")
    return confirm == 'BORRAR'

def main():
    """Función principal del verificador de USB."""
    print("--- Verificador de Capacidad Real de USB ---")
    
    drive_path = get_drive_letter()
    
    if not os.path.isdir(drive_path):
        print(f"Error: La unidad '{drive_path}' no parece ser un directorio válido o no está accesible.")
        sys.exit(1)
        
    if not confirm_destruction(drive_path):
        print("Confirmación no recibida. Abortando la operación.")
        sys.exit(0)
        
    print(f"Iniciando la verificación en {drive_path}...")
    
    total_gb_written, files_written, data_chunk = write_phase(drive_path)
    
    if not files_written:
        print("No se pudo escribir ningún dato. Verifica que la unidad no esté protegida contra escritura.")
        sys.exit(1)
        
    print(f"\nFase de escritura completada.")
    print(f"Se escribieron un total de {total_gb_written} GB en {len(files_written)} archivos.")
    
    print("\nIniciando fase de verificación...")
    verified_gb = verify_phase(files_written, data_chunk)
    
    print("\n--- REPORTE FINAL ---")
    print(f"Capacidad verificada exitosamente: {verified_gb} GB")
    print(f"Capacidad reportada por el sistema (aprox): {total_gb_written} GB")
    
    if verified_gb < total_gb_written:
        print("¡ALERTA! La unidad parece ser FALSA o está DAÑADA.")
        print(f"La corrupción de datos empezó a ocurrir después de escribir {verified_gb} GB.")
    else:
        print("La unidad parece ser genuina. La capacidad verificada coincide con la escrita.")

    cleanup_phase(files_written)

    print("\nProceso finalizado.")


def cleanup_phase(files_to_delete):
    """Pregunta al usuario si desea eliminar los archivos de prueba."""
    print("\n" + "-"*50)
    while True:
        choice = input("¿Deseas eliminar los archivos de prueba creados en la unidad? (s/n): ").strip().lower()
        if choice in ['s', 'si']:
            print("Eliminando archivos de prueba...")
            for file_path in files_to_delete:
                try:
                    os.remove(file_path)
                    print(f"Eliminado: {os.path.basename(file_path)}")
                except OSError as e:
                    print(f"Error al eliminar {os.path.basename(file_path)}: {e}")
            print("Limpieza completada.")
            break
        elif choice in ['n', 'no']:
            print("Los archivos de prueba no se eliminarán.")
            break
        else:
            print("Respuesta inválida. Por favor, responde 's' o 'n'.")


def verify_file(file_path, original_data_chunk):
    """Verifica la integridad de un único archivo."""
    chunk_size = len(original_data_chunk)
    try:
        with open(file_path, "rb") as f:
            while True:
                read_chunk = f.read(chunk_size)
                if not read_chunk:
                    break  # Fin del archivo
                
                if read_chunk != original_data_chunk[:len(read_chunk)]:
                    print("¡CORRUPCIÓN DE DATOS DETECTADA!")
                    return False
        return True
    except IOError as e:
        print(f"\nError de E/S al leer el archivo: {e}")
        return False


def verify_phase(files_to_verify, original_data_chunk):
    """
    Verifica la integridad de los archivos escritos.

    Returns:
        int: Total de GB verificados exitosamente.
    """
    total_gb_verified = 0
    
    for file_path in files_to_verify:
        print(f"Verificando {os.path.basename(file_path)}... ", end="", flush=True)
        if verify_file(file_path, original_data_chunk):
            total_gb_verified += 1 # Asumimos archivos de 1GB
            print(f"OK. ({total_gb_verified}GB verificados)")
        else:
            # El mensaje de corrupción se imprime dentro de verify_file
            return total_gb_verified
            
    return total_gb_verified


def write_phase(drive_path):
    """
    Escribe archivos de 1GB en la unidad hasta que se llene.
    
    Returns:
        Tuple[int, List[str], bytes]: Total de GB escritos, la lista de archivos creados y el chunk de datos.
    """
    chunk_size_mb = 1
    writes_per_gb = 1024 // chunk_size_mb
    file_size_gb = 1

    # Creamos un chunk de datos de 1MB para reutilizar
    print(f"Creando un bloque de datos de prueba de {chunk_size_mb}MB...")
    # Un patrón simple pero no trivial
    data_chunk = (b"Gemini USB Capacity Test Pattern. " * (1024 * 1024 // 32))[:chunk_size_mb * 1024 * 1024]

    files_written = []
    total_gb_written = 0
    file_index = 1

    print("Iniciando fase de escritura. Esto puede tardar MUCHO tiempo...")

    while True:
        file_path = os.path.join(drive_path, f"test_file_{file_index}.bin")
        try:
            print(f"Escribiendo archivo {file_index} ({file_size_gb}GB)... ", end="", flush=True)
            with open(file_path, "wb") as f:
                for i in range(writes_per_gb):
                    f.write(data_chunk)
            
            print("Verificando... ", end="", flush=True)
            if not verify_file(file_path, data_chunk):
                print(f"\nError: Corrupción de datos detectada en el archivo recién escrito: {os.path.basename(file_path)}")
                print("La unidad podría ser falsa o estar dañada. Deteniendo la escritura.")
                try:
                    os.remove(file_path)
                except OSError as e:
                    print(f"No se pudo eliminar el archivo corrupto: {e}")
                break

            files_written.append(file_path)
            total_gb_written += file_size_gb
            print(f"OK. ({total_gb_written}GB en total)")
            file_index += 1

        except IOError as e:
            print(f"\nError de E/S: {e}. La unidad probablemente está llena.")
            print("Deteniendo la fase de escritura.")
            break
            
    return total_gb_written, files_written, data_chunk

if __name__ == "__main__":
    main()
