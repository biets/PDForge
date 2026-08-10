from pypdf import PdfReader

def conta_pagine(percorso_file):
    """Restituisce il numero di pagine di un PDF."""
    lettore = PdfReader(percorso_file)
    return len(lettore.pages)


# Blocco eseguito solo se lanci questo file direttamente
if __name__ == "__main__":
    risultato = conta_pagine("test.pdf")
    print(f"Il PDF ha {risultato} pagine")