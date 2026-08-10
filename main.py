print("Questo è il mio progetto PDForge!")

# Variabili di base
nome_file = "documento.pdf"
numero_pagine = 12
dimensione_mb = 2.5
è_protetto = False

# print() stampa a schermo
print(nome_file)
print(numero_pagine)

# f-string: il modo moderno per costruire messaggi con variabili dentro
print(f"Il file {nome_file} ha {numero_pagine} pagine ed è {dimensione_mb} MB")

file_utente = input("Inserisci il nome di un file PDF: ")
print(f"Hai inserito: {file_utente}")