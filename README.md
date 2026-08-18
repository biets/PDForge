<p align="center">
  <img src="assets/logo.png" width="120" alt="Icona PDForge">
</p>

# PDForge

**PDForge** è un'applicazione desktop per la gestione rapida dei file PDF: unione, separazione, compressione e rotazione, il tutto in un'unica app leggera e semplice da usare.
Il progetto nasce anche come percorso di apprendimento di Python.

👤 **Autore:** Fabio Di Terlizzi ([@biets](https://github.com/biets))

![Screenshot dell'applicazione](assets/screenshot.png)

---

## ✨ Funzionalità

- ✅ **Unione PDF** — combina più file PDF in un unico documento, con riordino manuale dei file prima dell'unione
- ✅ **Separazione PDF** — estrae singole pagine o intervalli da un PDF, in un unico file o uno per pagina
- ✅ **Compressione PDF** — riduce il peso dei file ricomprimendo le immagini incorporate, con slider per regolare la qualità
- ✅ **Rotazione pagine** — ruota una o più pagine di un documento (90°, 180°, 270°)
- ✅ **Conteggio pagine** — utility di lettura rapida dei metadati del PDF
- ✅ **Gestione lista file** — aggiunta, rimozione e riordino dei file prima di eseguire un'operazione
- ✅ **Feedback durante le operazioni** — barra di progresso e pulsanti disabilitati mentre un'operazione è in corso, grazie all'esecuzione in background (threading)

> Legenda: ✅ completato · 🔧 in sviluppo

---

## 🛠️ Tecnologie utilizzate

- **Python 3** — linguaggio principale
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** — interfaccia grafica
- **[pypdf](https://pypdf.readthedocs.io/)** — manipolazione PDF (unione, separazione, rotazione)
- **[pikepdf](https://pikepdf.readthedocs.io/)** — compressione avanzata
- **[Pillow](https://pillow.readthedocs.io/)** — ricompressione delle immagini incorporate e gestione icone

---

## 📁 Struttura del progetto

```
PDForge/
├── core/                   # Logica di business (nessuna dipendenza dalla GUI)
│   ├── read_pdf.py         # Lettura metadati (conta_pagine)
│   ├── merge_pdf.py        # Unione PDF
│   ├── split_pdf.py        # Separazione PDF
│   ├── compress_pdf.py     # Compressione immagini
│   └── rotate_pdf.py       # Rotazione pagine
├── gui/                    # Interfaccia grafica (CustomTkinter)
│   └── gui.py
├── assets/                 # Icone e immagini dell'app
├── tests_files/             # File PDF di prova (non versionato)
├── main.py                 # Entry point dell'applicazione
├── requirements.txt        # Dipendenze del progetto
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

---

## 🗺️ Roadmap

- [ ] Packaging dell'applicazione in eseguibile standalone (.exe)
- [ ] Test automatizzati sui moduli `core/`
- [ ] Refactoring della GUI in una classe (da variabili globali a `self.widget_name`)
- [ ] Drag & drop per il riordino dei file

---

## 🤝 Contributi

Progetto personale a scopo di apprendimento — suggerimenti e feedback sono comunque benvenuti tramite issue.

## 📄 Licenza

Distribuito con licenza [MIT](LICENSE).