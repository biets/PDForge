from pypdf import PdfReader, PdfWriter

def split_pdf(percorso_file, cartella_output, pagine=None, modalita="separato"):
    """
    Separa un PDF.
    
    pagine: lista di numeri di pagina (1-indexed) da estrarre. Se None, prende tutte le pagine.
    modalita: "separato" = un file per ogni pagina, "singolo" = un unico file con le pagine scelte
    """
    lettore = PdfReader(percorso_file)
    totale_pagine = len(lettore.pages)

    # Se non specificato, lavoriamo su tutte le pagine (comportamento originale)
    if pagine is None:
        indici = range(totale_pagine)
    else:
        # Convertiamo da numerazione "umana" (1,2,3...) a indice Python (0,1,2...)
        indici = [p - 1 for p in pagine]

    if modalita == "separato":
        for indice in indici:
            writer = PdfWriter()
            writer.add_page(lettore.pages[indice])
            nome_output = f"{cartella_output}/pagina_{indice + 1}.pdf"
            with open(nome_output, "wb") as output:
                writer.write(output)

    elif modalita == "singolo":
        writer = PdfWriter()
        for indice in indici:
            writer.add_page(lettore.pages[indice])
        nome_output = f"{cartella_output}/pagine_selezionate.pdf"
        with open(nome_output, "wb") as output:
            writer.write(output)


if __name__ == "__main__":
    split_pdf("../tests_files/test.pdf", "../tests_files")
    print("PDF separato con successo!")