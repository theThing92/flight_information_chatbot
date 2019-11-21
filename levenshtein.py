# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np

def levenshtein(seq1, seq2):
    # Legt die Menge der Zeilen der Matrix fest
    size_x = len(seq1) + 1
    #legt die Menge der Spalten der Matrix fest
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    #Erstellen der "leeren Matrix"
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y
    #Füllen der Matrix
    for x in range(1, size_x):
        for y in range(1, size_y):
            #Übereinstimmung
            if seq1[x-1] == seq2[y-1]:
                # Matrixwerte werden erhöht; Hauptdiagonale nicht
                # Minimalwert der 2 Optionen
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            #Vertauschung wird nur 1x gewertet
            elif seq1[x-2] == seq2[y-1] and seq1[x-1] == seq2[y-2]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            #Abweichung
            else:
                # Matrixwerte werden erhöht inkl. Hauptdiagonale
                # Minimalwert der 3 Optionen
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    #Der Wert unten rechts ist die levenshteindistanz
    return (matrix[size_x - 1, size_y - 1])

eingabe = "Hongong"
# ontology
ontology = ("Hongkong", "New York", "Berlin")
distanz = {}
# Wie hoch ist die akzeptiere Levenshtein-Distanz
fehlergrenze = 3
''' Worte deren Levenshteindistanz zur Eingabe unter der gegebenen 
Fehlergrenze liegt werden in das distanz-Lexikon aufgenommen'''
for element in ontology:
    if levenshtein(eingabe,element)<=fehlergrenze:
        distanz[element] = levenshtein(eingabe,element)
print(distanz)    

# Vertauschung nachträglich eingebaut
# Groß-/ Kleinschreibung wird als voller Fehler gewertet
# Tastendistanz läuft nicht mit ein (Levenstheindistanz anpassen)
# höhere Fehlergrenze bei längeren Worten/ höhere Häufigkeit
# Silbenstruktur 
