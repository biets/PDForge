from pypdf import PdfReader, PdfWriter

def merge_pdf(lista_file, file_output):
    """Unisce più file PDF in un unico file di output."""
    writer = PdfWriter()

    # Scorriamo ogni file della lista e aggiungiamo le sue pagine
    for percorso_file in lista_file:
        lettore = PdfReader(percorso_file)
        for pagina in lettore.pages:
            writer.add_page(pagina)

    # Salviamo il risultato finale su disco
    with open(file_output, "wb") as output:
        writer.write(output)


if __name__ == "__main__":
    file_da_unire = ["test.pdf", "test2.pdf"]
    merge_pdf(file_da_unire, "risultato_unito.pdf")
    print("PDF uniti con successo!")