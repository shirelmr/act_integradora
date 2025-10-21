class SubstrRank:
    def __init__(self, left_rank=0, right_rank=0, index=0):
        self.left_rank = left_rank
        self.right_rank = right_rank
        self.index = index

def make_ranks(substr_rank, n):
    r = 0
    rank = [-1] * n
    rank[substr_rank[0].index] = r
    
    for i in range(1, n):
        if (substr_rank[i].left_rank != substr_rank[i-1].left_rank or
            substr_rank[i].right_rank != substr_rank[i-1].right_rank):
            r += 1
        rank[substr_rank[i].index] = r
    return rank

def suffix_array(T):
    n = len(T)
    
    chars = sorted(set(T))
    char_rank = {c: i for i, c in enumerate(chars)}
    
    substr_rank = []
    for i in range(n):
        substr_rank.append(SubstrRank(
            char_rank[T[i]], 
            char_rank[T[i + 1]] if i < n - 1 else -1,
            i
        ))

    substr_rank.sort(key=lambda sr: (sr.left_rank, sr.right_rank))

    l = 1
    while l < n:
        rank = make_ranks(substr_rank, n)

        for i in range(n):
            next_index = substr_rank[i].index + l
            substr_rank[i].left_rank = rank[substr_rank[i].index]
            substr_rank[i].right_rank = rank[next_index] if next_index < n else -1

        substr_rank.sort(key=lambda sr: (sr.left_rank, sr.right_rank))
        l *= 2

    SA = [substr_rank[i].index for i in range(n)]

    return SA

# ============================================================================
# PUNTO 4: BSQUEDA DE SUBCADENAS USANDO SUFFIX ARRAY
# Implementa búsqueda binaria según el algoritmo de Manber-Myers
# Retorna TODAS las posiciones donde aparece el PATRON
# ============================================================================

def search_all_occurrences(text, SA, pattern):
  
    n = len(SA)
    m = len(pattern)
    occurrences = []
    
    left = 0
    right = n
    
    while left < right:
        mid = (left + right) // 2
        suffix_start = SA[mid]
        
        if suffix_start + m <= len(text):
            suffix = text[suffix_start:suffix_start + m]
        else:
            suffix = text[suffix_start:]
        
        if suffix < pattern:
            left = mid + 1
        else:
            right = mid
    
    start = left
    while start < n:
        suffix_start = SA[start]
        if suffix_start + m <= len(text):
            suffix = text[suffix_start:suffix_start + m]
            if suffix == pattern:
                occurrences.append(suffix_start)
                start += 1
            else:
                break
        else:
            break
    
    return sorted(occurrences)

# ============================================================================
# FIN PUNTO 4
# ============================================================================

def main(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    
    SA = suffix_array(text)
    
    pattern = "monster"
    positions = search_all_occurrences(text, SA, pattern)
    
    print(f"Patron: '{pattern}'")
    print(f"Ocurrencias: {len(positions)}")
    
    if positions:
        print(f"Todas las posiciones: {positions}")
    else:
        print("No se encontraron ocurrencias")
    
    return SA

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "frankenstein.txt"
    
    SA = main(filename)