import pikepdf
import os

def comprimi_pdf_avanzato(percorso_file, file_output):
    """Comprime un PDF sfruttando le ottimizzazioni integrate di pikepdf/QPDF."""
    pdf = pikepdf.open(percorso_file)

    # compress_streams comprime i flussi di contenuto
    # object_stream_mode raggruppa gli oggetti interni in flussi condivisi
    pdf.save(
        file_output,
        compress_streams=True,
        object_stream_mode=pikepdf.ObjectStreamMode.generate,
    )
    pdf.close()


if __name__ == "__main__":
    percorso_input = "../tests_files/test.pdf"
    percorso_output = "../tests_files/test_compresso_avanzato.pdf"

    comprimi_pdf_avanzato(percorso_input, percorso_output)

    dimensione_originale = os.path.getsize(percorso_input)
    dimensione_finale = os.path.getsize(percorso_output)
    percentuale = (1 - dimensione_finale / dimensione_originale) * 100

    print(f"Dimensione originale: {dimensione_originale} byte")
    print(f"Dimensione compressa: {dimensione_finale} byte")
    print(f"Risparmio: {percentuale:.1f}%")