import time
import os
from memory_profiler import profile
import sais
import manber_myers

# Lista de libros ordenados aproximadamente por tamaño
BOOKS = [
    "romeo_and_juliet.txt",
    "frankenstein.txt",
    "pride_and_prejudice.txt",
    "alices_adventures.txt",
    "murder_in_the_gilded_cage.txt"
]

def get_file_size(filename):
    """Retorna el tamaño del archivo en MB"""
    return os.path.getsize(filename) / (1024 * 1024)

@profile
def test_sais(filename):
    """Prueba el algoritmo SAIS con un archivo"""
    start_time = time.time()
    SA = sais.main(filename)
    end_time = time.time()
    return len(SA), end_time - start_time

@profile
def test_manber_myers(filename):
    """Prueba el algoritmo Manber-Myers con un archivo"""
    start_time = time.time()
    SA = manber_myers.main(filename)
    end_time = time.time()
    return len(SA), end_time - start_time

def print_separator():
    print("="*80)

def test_book(book):
    """Prueba un libro individual con ambos algoritmos"""
    size = get_file_size(book)
    print_separator()
    print(f"Libro: {book}")
    print(f"Tamaño: {size:.2f} MB")
    print_separator()
    
    # Prueba SAIS
    print("\nEjecutando SAIS...")
    try:
        sa_len, time_sais = test_sais(book)
        print(f"✓ SAIS completado:")
        print(f"  - Tiempo: {time_sais:.2f} segundos")
        print(f"  - Longitud del Suffix Array: {sa_len}")
    except Exception as e:
        print(f"✗ Error en SAIS: {str(e)}")
    
    # Prueba Manber-Myers
    print("\nEjecutando Manber-Myers...")
    try:
        sa_len, time_mm = test_manber_myers(book)
        print(f"✓ Manber-Myers completado:")
        print(f"  - Tiempo: {time_mm:.2f} segundos")
        print(f"  - Longitud del Suffix Array: {sa_len}")
    except Exception as e:
        print(f"✗ Error en Manber-Myers: {str(e)}")

def main():
    print("\nBenchmark de Algoritmos de Suffix Array")
    print("Comparando SAIS vs Manber-Myers")
    print("\nNota: El uso de memoria se mostrará por el decorador @profile")
    
    for book in BOOKS:
        test_book(book)
        print("\n")  # Espacio extra entre libros

if __name__ == "__main__":
    main()