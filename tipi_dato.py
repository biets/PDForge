# type() ci dice il tipo di una variabile
nome = "documento.pdf"
pagine = 12
dimensione = 2.5
protetto = False

print(type(nome))       # <class 'str'>
print(type(pagine))     # <class 'int'>
print(type(dimensione)) # <class 'float'>
print(type(protetto))   # <class 'bool'>

pagine_inserite = input("Quante pagine ha il tuo PDF? ")
print(type(pagine_inserite))  # <class 'str'>, anche se hai scritto un numero!

# Questo causerebbe un errore se provassimo a fare matematica:
#pagine_totali = pagine_inserite + 5   # ❌ TypeError!

# Dobbiamo convertire esplicitamente in intero:
pagine_numero = int(pagine_inserite)
pagine_totali = pagine_numero + 5
print(f"Pagine totali dopo la conversione: {pagine_totali}")