numero_pagine = 15
dimensione_mb = 8.2

# if semplice
if numero_pagine > 10:
    print("Il documento è abbastanza lungo")

# if / else
if dimensione_mb > 5:
    print("File pesante, valuta la compressione")
else:
    print("File di dimensioni ok")

# if / elif / else (più condizioni in fila)
if numero_pagine <= 5:
    print("Documento breve")
elif numero_pagine <= 20:
    print("Documento medio")
else:
    print("Documento lungo")

# validazione: il caso limite di ieri!
def pagine_rimanenti(pagine_totali, pagine_lette):
    if pagine_lette > pagine_totali:
        print("Errore: hai letto più pagine di quelle totali")
        return None
    return pagine_totali - pagine_lette

print(pagine_rimanenti(20, 7))
print(pagine_rimanenti(20, 25))


# for su una lista di nomi file (le liste le vediamo bene domani, per ora usale così)
file_pdf = ["report.pdf", "fattura.pdf", "contratto.pdf"]

for file in file_pdf:
    print(f"Sto elaborando: {file}")

# for con range() - utile per "ripeti N volte" o "per ogni pagina da 1 a N"
for numero_pagina in range(1, 6):
    print(f"Elaboro pagina {numero_pagina}")

# for con range() - esercizio per stampare solo i numeri pari
print ("ESERCIZIO: stampare solo i numeri pari da 1 a 11")
for x in range(1, 11):
    print(f"numero pari {x}")
    #if x % 2 == 0:
        #print(f"numero pari {x}")
