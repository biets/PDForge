def saluta_utente(nome):
    print(f"Ciao {nome}, benvenuto in PDForge!")

def calcola_dimensione_totale(dimensione1, dimensione2):
    totale = dimensione1 + dimensione2
    return totale

def descrivi_pdf(nome_file, numero_pagine):
    descrizione = f"Il file {nome_file} ha {numero_pagine} pagine"
    return descrizione

def pagine_rimanenti(pagine_totali, pagine_lette):
    rimanenti = pagine_totali - pagine_lette
    return rimanenti


# Chiamare (usare) le funzioni:
saluta_utente("Fabio")

somma = calcola_dimensione_totale(2.5, 3.1)
print(f"Dimensione totale: {somma} MB")

risultato = descrivi_pdf("report.pdf", 25)
print(risultato)

pagine_rimanenti = pagine_rimanenti(25, 10)
print(f"Pagine rimanenti: {pagine_rimanenti}")