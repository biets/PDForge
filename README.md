# <img src="icons/icona_pdforge.ico" width="32" height="32" alt="Icona PDForge"> PDForge

**PDForge** è un'applicazione desktop con interfaccia grafica per la gestione rapida dei file PDF: unione, separazione, compressione e altre utilità, il tutto in un'unica app leggera e semplice da usare.

Il progetto nasce anche come percorso di apprendimento pratico di Python, Git/GitHub e sviluppo di applicazioni desktop.

👤 **Autore:** Fabio ([@biets](https://github.com/biets))

![Screenshot dell'applicazione](assets/screenshot.png)
> 💡 Sostituisci `assets/screenshot.png` con uno screenshot reale della tua GUI (crea la cartella `assets/` nella root del progetto).

---

## ✨ Funzionalità

- ✅ **Unione PDF** — combina più file PDF in un unico documento
- ✅ **Separazione PDF** — estrae singole pagine o intervalli da un PDF (file singolo o output separati)
- ✅ **Compressione PDF** — riduce il peso dei file ricomprimendo le immagini incorporate a qualità regolabile
- ✅ **Rotazione pagine** — ruota una o più pagine di un documento, con selezione angolo e pagine specifiche
- ✅ **Conteggio pagine** — utility di lettura rapida dei metadati del PDF

> Legenda: ✅ completato · 🔧 in sviluppo

---

## 🛠️ Tecnologie utilizzate

- **Python 3** — linguaggio principale
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** — interfaccia grafica moderna
- **[pypdf](https://pypdf.readthedocs.io/)** — manipolazione PDF (unione, separazione, compressione stream)
- **[pikepdf](https://pikepdf.readthedocs.io/)** — compressione avanzata
- **[Pillow](https://pillow.readthedocs.io/)** — ricompressione delle immagini incorporate

---

## 📁 Struttura del progetto

```
PDForge/
├── core/                       # Logica di business (nessuna dipendenza dalla GUI)
│   ├── read_pdf.py             # Lettura metadati (conta_pagine)
│   ├── merge_pdf.py            # Unione PDF
│   ├── split_pdf.py            # Separazione PDF
│   ├── compress_pdf.py         # Compressione (stream + immagini incorporate)
│   └── rotate_pdf.py           # Rotazione pagine
├── gui/
│   └── gui.py                  # Interfaccia grafica (CustomTkinter) e collegamento al core
├── assets/
│   ├── icona_pdforge.ico       # Icona finestra applicazione
│   ├── icona_pdforge_256.png   # Icona mostrata nella sidebar
│   ├── screenshot.png          # Screenshot per il README
│   └── icons/                  # Icone dei pulsanti (merge, split, compress, rotate)
├── tests_files/                # File PDF di prova (esclusi dal repository)
├── main.py                     # Entry point dell'applicazione
├── requirements.txt            # Dipendenze del progetto
└── README.md
```

---

## 🚀 Installazione

```bash
# Clona il repository
git clone https://github.com/biets/PDForge.git
cd PDForge

# Crea un ambiente virtuale (consigliato)
python -m venv venv
venv\Scripts\activate      # Windows

# Installa le dipendenze
pip install -r requirements.txt
```

## ▶️ Utilizzo

```bash
python main.py
```

Seleziona i file PDF dall'interfaccia, scegli l'operazione desiderata (unione, separazione, compressione...) e avvia l'elaborazione.

---

## 🗺️ Roadmap

Tutte le operazioni core (unione, separazione, compressione, rotazione) sono implementate e collegate alla GUI. Il lavoro attuale è concentrato sul restyling dell'interfaccia:

- [x] Layout a due colonne (sidebar + area principale)
- [x] Controlli condizionali (slider qualità, selettore angolo) mostrati solo per l'operazione selezionata
- [ ] Stile di evidenziazione per il pulsante attivo/selezionato
- [ ] Icone sui pulsanti
- [ ] Packaging dell'applicazione in eseguibile standalone (.exe)
- [ ] Test automatizzati

---

## 🤝 Contributi

Progetto personale a scopo di apprendimento — suggerimenti e feedback sono comunque benvenuti tramite issue.

## 📄 Licenza

Distribuito con licenza [MIT](LICENSE).
