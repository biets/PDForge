from pypdf import PdfReader, PdfWriter

def rotate_pdf(percorso_file, angolo, percorso_output):
    """
    Ruota tutte le pagine di un PDF di un angolo specificato.
    L'angolo deve essere un multiplo di 90 (90, 180, 270, -90, ecc.)
    """
    # Leggiamo il file originale
    lettore = PdfReader(percorso_file)
    scrittore = PdfWriter()

    # Cicliamo su ogni pagina, la ruotiamo e la aggiungiamo al nuovo writer
    for pagina in lettore.pages:
        pagina.rotate(angolo)
        scrittore.add_page(pagina)

    # Salviamo il risultato nel file di output
    with open(percorso_output, "wb") as file_output:
        scrittore.write(file_output)

    return True