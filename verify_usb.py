
import os
import sys
import time
import hashlib

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
    
    total_gb_written, files_written, expected_md5 = write_phase(drive_path)
    
    if not files_written:
        print("No se pudo escribir ningún dato. Verifica que la unidad no esté protegida contra escritura.")
        sys.exit(1)
        
    print(f"\nFase de escritura completada.")
    print(f"Se escribieron un total de {total_gb_written} GB en {len(files_written)} archivos.")
    
    print("\nIniciando fase de verificación final (re-lectura y MD5)...")
    verified_gb = verify_phase(files_written, expected_md5)
    
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


def calculate_file_md5(file_path, chunk_size=8192):
    """Calcula el hash MD5 de un archivo."""
    hasher = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        print(f"\nError de E/S al leer el archivo para calcular MD5: {e}")
        return None

def verify_phase(files_to_verify, expected_md5):
    """
    Verifica la integridad de los archivos escritos comparando su hash MD5.
    """
    total_gb_verified = 0
    for file_path in files_to_verify:
        print(f"Verificando {os.path.basename(file_path)}... ", end="", flush=True)
        actual_md5 = calculate_file_md5(file_path)
        if actual_md5 and actual_md5 == expected_md5:
            total_gb_verified += 1
            print(f"OK. ({total_gb_verified}GB verificados)")
        else:
            print("¡CORRUPCIÓN DE DATOS DETECTADA! (Hash MD5 no coincide)")
            if actual_md5:
                print(f"  - Esperado: {expected_md5}")
                print(f"  - Obtenido: {actual_md5}")
            return total_gb_verified
    return total_gb_verified

def write_phase(drive_path):
    """
    Escribe archivos de 1GB en la unidad hasta que se llene, verificando con MD5.
    """
    chunk_size_mb = 1
    writes_per_gb = 1024 // chunk_size_mb
    file_size_gb = 1

    print(f"Creando un bloque de datos de prueba de {chunk_size_mb}MB...")
    data_chunk = (b"Gemini USB Capacity Test Pattern. " * (1024 * 1024 // 32))[:chunk_size_mb * 1024 * 1024]

    print("Calculando hash MD5 de referencia para 1GB... ", end="", flush=True)
    md5_hasher = hashlib.md5()
    for _ in range(writes_per_gb):
        md5_hasher.update(data_chunk)
    expected_md5 = md5_hasher.hexdigest()
    print("OK.")
    print(f"  - Hash MD5 esperado: {expected_md5}")

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
            
            print("Verificando con MD5... ", end="", flush=True)
            actual_md5 = calculate_file_md5(file_path)

            if not actual_md5 or actual_md5 != expected_md5:
                print(f"\nError: Corrupción de datos detectada en el archivo recién escrito: {os.path.basename(file_path)}")
                print("La unidad podría ser falsa o estar dañada. Deteniendo la escritura.")
                if actual_md5:
                    print(f"  - Esperado: {expected_md5}")
                    print(f"  - Obtenido: {actual_md5}")
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
            
    return total_gb_written, files_written, expected_md5

if __name__ == "__main__":
    main()
