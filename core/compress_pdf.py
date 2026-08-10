from pypdf import PdfReader, PdfWriter

def comprimi_pdf(percorso_file, file_output):
    """Comprime un PDF riducendo gli stream di contenuto e rimuovendo duplicati."""
    lettore = PdfReader(percorso_file)
    writer = PdfWriter()

    # Prima aggiungiamo tutte le pagine al writer
    for pagina in lettore.pages:
        writer.add_page(pagina)

    # Solo ORA possiamo comprimere: lavoriamo sulle pagine del writer, non del lettore
    for pagina in writer.pages:
        pagina.compress_content_streams()

    # Rimuove immagini/font duplicati nel documento
    writer.compress_identical_objects()

    with open(file_output, "wb") as output:
        writer.write(output)


if __name__ == "__main__":
    import os

    percorso_input = "../tests_files/test.pdf"
    percorso_output = "../tests_files/test_compresso.pdf"

    comprimi_pdf(percorso_input, percorso_output)

    # Confrontiamo le dimensioni prima/dopo, per vedere se ha funzionato davvero
    dimensione_originale = os.path.getsize(percorso_input)
    dimensione_finale = os.path.getsize(percorso_output)

    print(f"Dimensione originale: {dimensione_originale} byte")
    print(f"Dimensione compressa: {dimensione_finale} byte")