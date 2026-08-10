# Spiegazione di liste e dizionari in Python

# LISTE
file_pdf = ["report.pdf", "fattura.pdf", "contratto.pdf"]

print(file_pdf)          # tutta la lista
print(file_pdf[0])       # primo elemento: report.pdf
print(file_pdf[1])       # secondo elemento: fattura.pdf
print(file_pdf[-1])      # ultimo elemento: contratto.pdf
print(len(file_pdf))     # quanti elementi ha: 3

# aggiungere un elemento
file_pdf.append("bolletta.pdf")
print(file_pdf)

# rimuovere un elemento
file_pdf.remove("fattura.pdf")
print(file_pdf)

# controllare se un elemento è presente
if "report.pdf" in file_pdf:
    print("report.pdf è nella lista")

# scorrere la lista con for (già visto ieri)
for file in file_pdf:
    print(f"File: {file}")

# DIZIONARI
documento = {
    "nome": "report.pdf",
    "pagine": 24,
    "dimensione_mb": 3.4,
    "protetto": False
}

print(documento["nome"])          # report.pdf
print(documento["pagine"])        # 24

# modificare un valore
documento["pagine"] = 25

# aggiungere una nuova chiave
documento["autore"] = "Fabio"

print(documento)

# scorrere un dizionario
for chiave, valore in documento.items():
    print(f"{chiave}: {valore}")