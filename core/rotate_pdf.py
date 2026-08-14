from pypdf import PdfReader, PdfWriter

def rotate_pdf(percorso_file, angolo, percorso_output, pagine=None):
    """
    Ruota le pagine di un PDF di un angolo specificato.
    Se 'pagine' è None, ruota tutte le pagine.
    Se 'pagine' è una lista di numeri (es. [1, 3, 5]), ruota solo quelle,
    lasciando le altre invariate. La numerazione parte da 1 (non da 0).
    """
    lettore = PdfReader(percorso_file)
    scrittore = PdfWriter()

    # enumerate(..., start=1) ci dà sia l'indice (a partire da 1) che la pagina,
    # così possiamo confrontarlo direttamente con i numeri scelti dall'utente
    for numero_pagina, pagina in enumerate(lettore.pages, start=1):
        if pagine is None or numero_pagina in pagine:
            pagina.rotate(angolo)
        scrittore.add_page(pagina)

    with open(percorso_output, "wb") as file_output:
        scrittore.write(file_output)

    return True