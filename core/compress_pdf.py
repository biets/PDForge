import pikepdf
from pikepdf import PdfImage, Name
from PIL import Image
import io
import os

def compress_pdf(percorso_file, file_output, qualita=50):
    """Ricomprime le immagini incorporate in un PDF come JPEG a qualità ridotta."""
    pdf = pikepdf.open(percorso_file)
    immagini_processate = 0

    for pagina in pdf.pages:
        for nome_immagine, oggetto_raw in pagina.images.items():
            immagine_pdf = PdfImage(oggetto_raw)

            try:
                # Convertiamo l'immagine PDF in un'immagine Pillow "normale"
                immagine_pil = immagine_pdf.as_pil_image()
            except Exception:
                # Alcune immagini (es. formati particolari) non sono convertibili: le saltiamo
                continue

            # JPEG non supporta trasparenza (RGBA) o palette (P), quindi convertiamo a RGB
            if immagine_pil.mode in ("RGBA", "P"):
                immagine_pil = immagine_pil.convert("RGB")

            # Salviamo l'immagine compressa in un "buffer", cioè in memoria, non su disco
            buffer = io.BytesIO()
            immagine_pil.save(buffer, format="JPEG", quality=qualita)
            buffer.seek(0)

            # Sostituiamo i dati originali dell'immagine nel PDF con quelli nuovi compressi
            oggetto_raw.write(buffer.read(), filter=Name("/DCTDecode"))
            immagini_processate += 1

    pdf.save(file_output, compress_streams=True)
    pdf.close()

    print(f"Immagini processate: {immagini_processate}")


if __name__ == "__main__":
    percorso_input = "../tests_files/test.pdf"
    percorso_output = "../tests_files/test_compresso_immagini.pdf"

    compress_pdf(percorso_input, percorso_output, qualita=50)

    dimensione_originale = os.path.getsize(percorso_input)
    dimensione_finale = os.path.getsize(percorso_output)
    percentuale = (1 - dimensione_finale / dimensione_originale) * 100

    print(f"Dimensione originale: {dimensione_originale} byte")
    print(f"Dimensione compressa: {dimensione_finale} byte")
    print(f"Risparmio: {percentuale:.1f}%")