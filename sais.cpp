#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <sstream>

using namespace std;

map<int, pair<int, int>> getBuckets(const vector<int>& T) {
    map<int, int> count;
    map<int, pair<int, int>> buckets;
    
    for (int c : T) {
        count[c]++;
    }
    
    int start = 0;
    for (auto& p : count) {
        int c = p.first;
        buckets[c] = make_pair(start, start + count[c]);
        start += count[c];
    }
    
    return buckets;
}

vector<int> sais(const vector<int>& T) {
    int n = T.size();
    
    // optimizatrion: vector<bool> en lugar de vector<char>
    // true = S-type, false = L-type
    vector<bool> t(n);
    
    t[n - 1] = true;  // 'S'
    
    for (int i = n - 1; i > 0; i--) {
        if (T[i-1] == T[i]) {
            t[i - 1] = t[i];
        } else {
            t[i - 1] = (T[i-1] < T[i]);  // true si S, false si L
        }
    }
    
    map<int, pair<int, int>> buckets = getBuckets(T);
    
    map<int, int> count;
    vector<int> SA(n, -1);
    map<int, int> LMS;
    int end = -1;
    
    // : t[i] en lugar de t[i] == 'S'
    for (int i = n - 1; i > 0; i--) {
        if (t[i] && !t[i - 1]) {  // S-type seguido de L-type
            int revoffset = ++count[T[i]];
            SA[buckets[T[i]].second - revoffset] = i;
            if (end != -1) {
                LMS[i] = end;
            }
            end = i;
        }
    }
    
    LMS[n - 1] = n - 1;
    
    count.clear();
    for (int i = 0; i < n; i++) {
        if (SA[i] >= 0) {
            if (SA[i] > 0 && !t[SA[i] - 1]) {  // L-type
                int symbol = T[SA[i] - 1];
                int offset = count[symbol];
                SA[buckets[symbol].first + offset] = SA[i] - 1;
                count[symbol] = offset + 1;
            }
        }
    }
    
    count.clear();
    for (int i = n - 1; i > 0; i--) {
        if (SA[i] > 0) {
            if (t[SA[i] - 1]) {  // S-type
                int symbol = T[SA[i] - 1];
                int revoffset = ++count[symbol];
                SA[buckets[symbol].second - revoffset] = SA[i] - 1;
            }
        }
    }
    
    vector<int> namesp(n, -1);
    int name = 0;
    int prev = -1;
    
    for (int i = 0; i < n; i++) {
        if (SA[i] >= 0 && t[SA[i]] && SA[i] > 0 && !t[SA[i] - 1]) {
            if (prev != -1 && SA[prev] >= 0) {
                int start1 = SA[prev];
                int end1 = LMS[SA[prev]];
                int start2 = SA[i];
                int end2 = LMS[SA[i]];
                
                bool different = false;
                if (end1 - start1 != end2 - start2) {
                    different = true;
                } else {
                    for (int j = 0; j <= end1 - start1; j++) {
                        if (T[start1 + j] != T[start2 + j]) {
                            different = true;
                            break;
                        }
                    }
                }
                
                if (different) {
                    name++;
                }
            }
            prev = i;
            namesp[SA[i]] = name;
        }
    }
    
    vector<int> names;
    vector<int> SApIdx;
    
    for (int i = 0; i < n; i++) {
        if (namesp[i] != -1) {
            names.push_back(namesp[i]);
            SApIdx.push_back(i);
        }
    }
    
    if (name < (int)names.size() - 1) {
        names = sais(names);
    }
    
    reverse(names.begin(), names.end());
    
    SA.assign(n, -1);
    count.clear();
    
    for (int i = 0; i < (int)names.size(); i++) {
        int pos = SApIdx[names[i]];
        int revoffset = ++count[T[pos]];
        SA[buckets[T[pos]].second - revoffset] = pos;
    }
    
    count.clear();
    for (int i = 0; i < n; i++) {
        if (SA[i] >= 0) {
            if (SA[i] > 0 && !t[SA[i] - 1]) {  // L-type
                int symbol = T[SA[i] - 1];
                int offset = count[symbol];
                SA[buckets[symbol].first + offset] = SA[i] - 1;
                count[symbol] = offset + 1;
            }
        }
    }
    
    count.clear();
    for (int i = n - 1; i > 0; i--) {
        if (SA[i] > 0) {
            if (t[SA[i] - 1]) {  // S-type
                int symbol = T[SA[i] - 1];
                int revoffset = ++count[symbol];
                SA[buckets[symbol].second - revoffset] = SA[i] - 1;
            }
        }
    }
    
    return SA;
}

string read_file(const string& filename) {
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error al abrir el archivo: " << filename << endl;
        exit(1);
    }
    
    stringstream buffer;
    buffer << file.rdbuf();
    string text = buffer.str();
    
    replace(text.begin(), text.end(), '\n', ' ');
    replace(text.begin(), text.end(), '\r', ' ');
    
    stringstream ss(text);
    string word, normalized;
    while (ss >> word) {
        if (!normalized.empty()) normalized += " ";
        normalized += word;
    }
    
    normalized += '$';
    
    return normalized;
}

// ============================================================================
// PUNTO 4: FUNCIÓN DE BÚSQUEDA DE SUBCADENAS USANDO SUFFIX ARRAY
// Implementa búsqueda binaria según el algoritmo de Manber-Myers
// Retorna TODAS las posiciones donde aparece el patrón
// ============================================================================

vector<int> search_all_occurrences(const string& text, const vector<int>& SA, const string& pattern) {
    int n = SA.size();
    int m = pattern.length();
    vector<int> occurrences;
    
    int left = 0;
    int right = n;
    
    while (left < right) {
        int mid = (left + right) / 2;
        int suffix_start = SA[mid];
        
        string suffix = "";
        if (suffix_start + m <= (int)text.length()) {
            suffix = text.substr(suffix_start, m);
        } else {
            suffix = text.substr(suffix_start);
        }
        
        if (suffix < pattern) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    
    int start = left;
    while (start < n) {
        int suffix_start = SA[start];
        
        if (suffix_start + m <= (int)text.length()) {
            string suffix = text.substr(suffix_start, m);
            
            if (suffix == pattern) {
                occurrences.push_back(suffix_start);
                start++;
            } else {
                break;
            }
        } else {
            break;
        }
    }
    
    sort(occurrences.begin(), occurrences.end());
    return occurrences;
}

// ============================================================================
// FIN PUNTO 4
// ============================================================================

int main(int argc, char* argv[]) {
    string filename = "frankenstein.txt";
    
    if (argc > 1) {
        filename = argv[1];
    }
    
    string text = read_file(filename);
    
    vector<int> T;
    for (char c : text) {
        T.push_back((int)c);
    }
    
    vector<int> SA = sais(T);
    
    string pattern = "monster";
    vector<int> positions = search_all_occurrences(text, SA, pattern);
    
    cout << "Patron: '" << pattern << "'" << endl;
    cout << "Ocurrencias: " << positions.size() << endl;
    
    if (positions.size() > 0) {
        cout << "Todas las posiciones: ";
        for (int i = 0; i < (int)positions.size(); i++) {
            cout << positions[i];
            if (i < (int)positions.size() - 1) cout << ", ";
        }
        cout << endl;
    }
    
    return 0;
}