def getBuckets(T):
    count = {}
    buckets = {}
    for c in T:
        count[c] = count.get(c, 0) + 1
    start = 0
    for c in sorted(count.keys()):
        buckets[c] = (start, start + count[c])
        start += count[c]
    return buckets

def sais(T):
    n = len(T)
    t = ["_"] * n
    
    t[n - 1] = "S"
    for i in range(n - 1, 0, -1):
        if T[i-1] == T[i]:
            t[i - 1] = t[i]
        else:
            t[i - 1] = "S" if T[i-1] < T[i] else "L"
    
    buckets = getBuckets(T)

    count = {}
    SA = [-1] * n
    LMS = {}
    end = None
    for i in range(n - 1, 0, -1):
        if t[i] == "S" and t[i - 1] == "L":
            revoffset = count[T[i]] = count.get(T[i], 0) + 1
            SA[buckets[T[i]][1] - revoffset] = i
            if end is not None:
                LMS[i] = end
            end = i

    LMS[n - 1] = n - 1
    
    # OPTIMIZACIÓN 1: usar clear() en lugar de crear nuevo diccionario
    count.clear()
    for i in range(n):
        if SA[i] >= 0:
            if SA[i] > 0 and t[SA[i] - 1] == "L":
                symbol = T[SA[i] - 1]
                offset = count.get(symbol, 0)
                SA[buckets[symbol][0] + offset] = SA[i] - 1
                count[symbol] = offset + 1

    # OPTIMIZACIÓN 1: usar clear() en lugar de crear nuevo diccionario
    count.clear()
    for i in range(n - 1, 0, -1):
        if SA[i] > 0:
            if t[SA[i] - 1] == "S":
                symbol = T[SA[i] - 1]
                revoffset = count[symbol] = count.get(symbol, 0) + 1
                SA[buckets[symbol][1] - revoffset] = SA[i] - 1

    namesp = [-1] * n
    name = 0
    prev = None
    for i in range(len(SA)):
        if SA[i] >= 0 and t[SA[i]] == "S" and SA[i] > 0 and t[SA[i] - 1] == "L":
            if prev is not None and SA[prev] >= 0:
                # OPTIMIZACIÓN 2: comparar longitudes antes de hacer slicing
                start1 = SA[prev]
                end1 = LMS[SA[prev]]
                start2 = SA[i]
                end2 = LMS[SA[i]]
                
                if end1 - start1 != end2 - start2:
                    name += 1
                elif T[start1:end1] != T[start2:end2]:
                    name += 1
            prev = i
            namesp[SA[i]] = name

    names = []
    SApIdx = []
    for i in range(n):
        if namesp[i] != -1:
            names.append(namesp[i])
            SApIdx.append(i)

    if name < len(names) - 1:
        names = sais(names)

    # OPTIMIZACIÓN 3: usar reverse() en lugar de list(reversed())
    names.reverse()

    SA = [-1] * n
    count = {}
    for i in range(len(names)):
        pos = SApIdx[names[i]]
        revoffset = count[T[pos]] = count.get(T[pos], 0) + 1
        SA[buckets[T[pos]][1] - revoffset] = pos

    count.clear()
    for i in range(n):
        if SA[i] >= 0:
            if SA[i] > 0 and t[SA[i] - 1] == "L":
                symbol = T[SA[i] - 1]
                offset = count.get(symbol, 0)
                SA[buckets[symbol][0] + offset] = SA[i] - 1
                count[symbol] = offset + 1

    count.clear()
    for i in range(n - 1, 0, -1):
        if SA[i] > 0:
            if t[SA[i] - 1] == "S":
                symbol = T[SA[i] - 1]
                revoffset = count[symbol] = count.get(symbol, 0) + 1
                SA[buckets[symbol][1] - revoffset] = SA[i] - 1

    return SA

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', ' ').replace('\r', '')
        text = ' '.join(text.split())
        text = text + '$'
        return text

def main(filename):
    text = read_file(filename)
    T = [ord(c) for c in text]
    return sais(T)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "frankenstein.txt"
    
    SA = main(filename)
    print(SA)