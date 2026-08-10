from pypdf import PdfReader, PdfWriter

def separa_pdf(percorso_file, cartella_output):
    """Separa un PDF in singoli file, una pagina per ciascuno."""
    lettore = PdfReader(percorso_file)

    # Scorriamo ogni pagina con il suo indice (0, 1, 2...)
    for indice, pagina in enumerate(lettore.pages):
        writer = PdfWriter()
        writer.add_page(pagina)

        # Costruiamo il nome del file di output, es. pagina_1.pdf
        nome_output = f"{cartella_output}/pagina_{indice + 1}.pdf"
        with open(nome_output, "wb") as output:
            writer.write(output)


if __name__ == "__main__":
    separa_pdf("../tests_files/test.pdf", "../tests_files")
    print("PDF separato con successo!")