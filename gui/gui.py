import webbrowser

import customtkinter as ctk
from tkinter import filedialog, messagebox  # messagebox per avvisi ed errori
from pypdf import PdfReader
from PIL import Image  # per la compressione delle immagini nei PDF
from customtkinter import CTkImage

file_selezionati = []
operazione_scelta = None
valore_qualita = 50  # valore di default della compressione
frame_controlli_qualita = None
frame_controlli_angolo = None
btn_unisci, btn_separa, btn_comprimi, btn_ruota = None, None, None, None

icone_bianche = {}  # dizionario: nome operazione -> CTkImage bianca
icone_nere = {}     # dizionario: nome operazione -> CTkImage nera
icona_rimuovi = None

# Variabile per tenere traccia dell'angolo scelto (default 90°)
angolo_scelto = None  # verrà creata come StringVar dentro avvia_gui(), dopo la creazione della finestra

def azione_unisci():
    global operazione_scelta
    operazione_scelta = "unisci"
    reset_color_btn()
    evidenzia_bottone(btn_unisci, "unisci")
    nascondi_controlli_extra()
    print("Operazione selezionata: Unisci PDF")

def azione_separa():
    global operazione_scelta
    operazione_scelta = "separa"
    reset_color_btn()
    evidenzia_bottone(btn_separa, "separa")
    nascondi_controlli_extra()
    print("Operazione selezionata: Separa PDF")

def azione_comprimi():
    global operazione_scelta
    operazione_scelta = "comprimi"
    nascondi_controlli_extra()
    reset_color_btn()
    evidenzia_bottone(btn_comprimi, "comprimi")
    frame_controlli_qualita.pack(pady=(20, 15), padx=20, fill="x")
    print("Operazione selezionata: Comprimi PDF")

def azione_ruota():
    global operazione_scelta
    operazione_scelta = "ruota"
    nascondi_controlli_extra()
    reset_color_btn()
    evidenzia_bottone(btn_ruota, "ruota")
    frame_controlli_angolo.pack(pady=(20, 20), padx=20)
    print("Operazione selezionata: Ruota pagine")

def nascondi_controlli_extra():
    """Nasconde entrambi i blocchi di controlli extra (qualità e angolo)."""
    frame_controlli_qualita.pack_forget()
    frame_controlli_angolo.pack_forget()

def reset_color_btn():
    """Riporta tutti i bottoni allo stato non selezionato."""
    coppie = [
        (btn_unisci, "unisci"),
        (btn_separa, "separa"),
        (btn_comprimi, "comprimi"),
        (btn_ruota, "ruota")
    ]
    for bottone, nome in coppie:
        bottone.configure(
            fg_color="transparent",
            text_color="white",
            hover_color="#444444",
            image=icone_bianche[nome]
        )

def evidenzia_bottone(bottone, nome_operazione):
    """Applica lo stato 'selezionato' a un bottone: sfondo pieno e icona scura."""
    bottone.configure(
        fg_color="white",
        text_color="#1a1a1a",
        hover_color="#e0e0e0",
        image=icone_nere[nome_operazione]
    )

def carica_icona_bicolore(percorso, dimensione=20):
    """
    Restituisce due CTkImage della stessa icona: una bianca e una nera.
    Serve perché i PNG hanno il colore fisso nei pixel: per cambiarlo
    non basta configurare il bottone, bisogna sostituire l'immagine.
    """
    originale = Image.open(percorso).convert("RGBA").resize((dimensione, dimensione))
    maschera = originale.getchannel("A")  # la "sagoma" dell'icona

    def tingi(colore_rgb):
        colorata = Image.new("RGBA", originale.size, colore_rgb + (255,))
        colorata.putalpha(maschera)
        return ctk.CTkImage(light_image=colorata, dark_image=colorata, size=(dimensione, dimensione))

    bianca = tingi((255, 255, 255))
    nera = tingi((26, 26, 26))  # non nero puro: si abbina meglio al testo #1a1a1a
    return bianca, nera

def carica_icona_singola(percorso, colore_rgb, dimensione=14):
    """Carica un'icona PNG e la tinge di un unico colore (RGB)."""
    originale = Image.open(percorso).convert("RGBA").resize((dimensione, dimensione))
    maschera = originale.getchannel("A")
    colorata = Image.new("RGBA", originale.size, colore_rgb + (255,))
    colorata.putalpha(maschera)
    return ctk.CTkImage(light_image=colorata, dark_image=colorata, size=(dimensione, dimensione))


from core.merge_pdf import merge_pdf # importiamo le funzioni core che implementano le operazioni sui PDF
from core.split_pdf import split_pdf
from core.compress_pdf import compress_pdf
from core.rotate_pdf import rotate_pdf
from tkinter import filedialog, messagebox, simpledialog  # aggiungiamo simpledialog

def esegui():
    # Controlli di sicurezza prima di agire
    if operazione_scelta is None:
        messagebox.showwarning("Attenzione", "Seleziona prima un'operazione")
        return

    if len(file_selezionati) == 0:
        messagebox.showwarning("Attenzione", "Aggiungi almeno un file PDF")
        return

    if operazione_scelta == "unisci":
            # Chiediamo dove salvare il PDF risultante
            percorso_output = filedialog.asksaveasfilename(
                title="Salva PDF unito come",
                defaultextension=".pdf",
                filetypes=[("File PDF", "*.pdf")]
            )

            # Se l'utente chiude la finestra senza scegliere, percorso_output è una stringa vuota
            if percorso_output == "":
                return

            # try/except: se qualcosa va storto (file corrotto, permessi, ecc.)
            # non vogliamo che il programma crashi, ma mostrare un errore gestito
            try:
                merge_pdf(file_selezionati, percorso_output)
                file_selezionati.clear()       # svuotiamo la lista dopo un merge riuscito
                aggiorna_lista_visiva()        # aggiorniamo la GUI per riflettere la lista vuota
                messagebox.showinfo("Completato", "PDF uniti con successo!")
            except Exception as errore:
                messagebox.showerror("Errore", f"Qualcosa è andato storto:\n{errore}")

    elif operazione_scelta == "separa":   
        if len(file_selezionati) > 1:
            messagebox.showwarning("Attenzione", "Per separare, seleziona un solo file PDF")
            return

        percorso_file = file_selezionati[0]
        totale_pagine = len(PdfReader(percorso_file).pages)

        # Chiediamo quali pagine estrarre (vuoto = tutte)
        testo_pagine = simpledialog.askstring(
            "Seleziona pagine",
            f"Il documento ha {totale_pagine} pagine.\nInserisci le pagine (es. 1,3,5-7) oppure lascia vuoto per tutte:"
        )

        # Se l'utente annulla il dialog, askstring ritorna None
        if testo_pagine is None:
            return

        try:
            if testo_pagine.strip() == "":
                pagine = None  # nessun filtro, tutte le pagine
            else:
                pagine = analizza_pagine(testo_pagine, totale_pagine)

            # Chiediamo la modalità solo se l'utente ha scelto pagine specifiche
            modalita = "separato"
            if pagine is not None:
                un_file_solo = messagebox.askyesno(
                    "Modalità",
                    "Vuoi un unico file con le pagine selezionate?\n\nSì = un solo PDF\nNo = un file per ogni pagina"
                )
                modalita = "singolo" if un_file_solo else "separato"

            cartella_output = filedialog.askdirectory(title="Scegli la cartella dove salvare")
            if cartella_output == "":
                return

            split_pdf(percorso_file, cartella_output, pagine=pagine, modalita=modalita)
            file_selezionati.clear()
            aggiorna_lista_visiva()
            messagebox.showinfo("Completato", "PDF separato con successo!")

        except ValueError as errore:
            messagebox.showerror("Errore", str(errore))
        except Exception as errore:
            messagebox.showerror("Errore", f"Qualcosa è andato storto:\n{errore}")
    elif operazione_scelta == "comprimi":
        if len(file_selezionati) > 1:
            messagebox.showwarning("Attenzione", "Per comprimere, seleziona un solo file PDF")
            return

        percorso_file = file_selezionati[0]

        # Chiediamo dove salvare il PDF compresso
        percorso_output = filedialog.asksaveasfilename(
            title="Salva PDF compresso come",
            defaultextension=".pdf",
            filetypes=[("File PDF", "*.pdf")]
        )

        if percorso_output == "":
            return

        try:
            compress_pdf(percorso_file, percorso_output, qualita=valore_qualita)
            file_selezionati.clear()
            aggiorna_lista_visiva()
            messagebox.showinfo("Completato", "PDF compresso con successo!")
        except Exception as errore:
            messagebox.showerror("Errore", f"Qualcosa è andato storto:\n{errore}")
    elif operazione_scelta == "ruota":
        if len(file_selezionati) > 1:
            messagebox.showwarning("Attenzione", "Per ruotare, seleziona un solo file PDF")
            return

        percorso_file = file_selezionati[0]
        angolo = int(angolo_scelto.get())
        totale_pagine = len(PdfReader(percorso_file).pages)

        # Chiediamo quali pagine ruotare (vuoto = tutte)
        testo_pagine = simpledialog.askstring(
            "Seleziona pagine",
            f"Il documento ha {totale_pagine} pagine.\nInserisci le pagine da ruotare (es. 1,3,5-7) oppure lascia vuoto per tutte:"
        )

        if testo_pagine is None:
            return

        try:
            if testo_pagine.strip() == "":
                pagine = None
            else:
                pagine = analizza_pagine(testo_pagine, totale_pagine)

            percorso_output = filedialog.asksaveasfilename(
                title="Salva PDF ruotato come",
                defaultextension=".pdf",
                filetypes=[("File PDF", "*.pdf")]
            )
            if percorso_output == "":
                return

            rotate_pdf(percorso_file, angolo, percorso_output, pagine=pagine)
            file_selezionati.clear()
            aggiorna_lista_visiva()
            messagebox.showinfo("Completato", "PDF ruotato con successo!")

        except ValueError as errore:
            messagebox.showerror("Errore", str(errore))
        except Exception as errore:
            messagebox.showerror("Errore", f"Qualcosa è andato storto:\n{errore}")
    else:
        messagebox.showinfo("In arrivo", "Questa operazione non è ancora collegata")

def aggiungi_file():
    # filedialog.askopenfilenames() apre la finestra di sistema
    # filetypes limita la scelta ai soli PDF
    # Attenzione al plurale "filenames": permette selezione multipla
    percorsi = filedialog.askopenfilenames(
        title="Seleziona i PDF",
        filetypes=[("File PDF", "*.pdf")]
    )
    
    # percorsi è una tupla (anche se scegli un solo file)
    # la scorriamo con un for, come hai già fatto con le liste
    for percorso in percorsi:
        file_selezionati.append(percorso)
    
    aggiorna_lista_visiva()

def rimuovi_file(percorso):
    """Rimuove un singolo file dalla lista e aggiorna la GUI."""
    file_selezionati.remove(percorso)
    aggiorna_lista_visiva()

def aggiorna_lista_visiva():
    # Puliamo il frame prima di ridisegnare (altrimenti si accumulano le label vecchie)
    for widget in frame_lista.winfo_children():
        widget.destroy()

    if len(file_selezionati) == 0:
        label = ctk.CTkLabel(frame_lista, text="Nessun file selezionato", text_color="gray")
        label.pack(anchor="w", padx=10, pady=(10, 10))
    else:
        for percorso in file_selezionati:
            # Ogni riga è un frame a sé: ci serve per affiancare label e bottone
            riga = ctk.CTkFrame(frame_lista, fg_color="transparent")
            riga.pack(fill="x", padx=10, pady=2)

            nome_file = percorso.split("/")[-1]
            label = ctk.CTkLabel(riga, text=nome_file)
            label.pack(side="left", anchor="w")

            btn_rimuovi = ctk.CTkButton(
                riga,
                text="",
                image=icona_rimuovi,
                width=24,
                height=24,
                fg_color="transparent",
                hover_color="#5a1a1a",
                command=lambda p=percorso: rimuovi_file(p)
            )
            btn_rimuovi.pack(side="right", padx=(0, 5))

def analizza_pagine(testo, totale_pagine):
    """Converte una stringa tipo '1,3,5-7' in una lista ordinata di numeri di pagina, senza duplicati."""
    pagine = set()  # usiamo un set per evitare duplicati automaticamente

    parti = testo.split(",")
    for parte in parti:
        parte = parte.strip()  # rimuove spazi accidentali
        if "-" in parte:
            inizio, fine = parte.split("-")
            inizio = int(inizio.strip())
            fine = int(fine.strip())
            pagine.update(range(inizio, fine + 1))
        else:
            pagine.add(int(parte))

    # Controllo di validità: le pagine devono esistere nel documento
    for numero in pagine:
        if numero < 1 or numero > totale_pagine:
            raise ValueError(f"La pagina {numero} non esiste (il documento ha {totale_pagine} pagine)")

    return sorted(pagine)

def aggiorna_qualita_e_label(valore, label):
    # aggiorna la variabile globale valore_qualita e il testo della label per la compressione
    global valore_qualita
    valore_qualita = int(valore)
    label.configure(text=f"Qualità compressione: {valore_qualita}")

def avvia_gui():
    global frame_lista, angolo_scelto, frame_controlli_qualita, frame_controlli_angolo
    global btn_unisci, btn_separa, btn_comprimi, btn_ruota
    global icone_bianche, icone_nere, icona_rimuovi

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("PDForge")
    app.iconbitmap("assets/icona_pdforge.ico")
    app.geometry("750x470")

    angolo_scelto = ctk.StringVar(value="90")

    # La finestra ha 2 colonne: sidebar fissa e area principale che si espande
    app.grid_columnconfigure(0, weight=0)
    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)  # riga del contenuto si espande in verticale
    app.grid_rowconfigure(1, weight=0)  # riga del footer resta fissa

    # Icone
    for nome, file_icona in [("unisci", "merge.png"), ("separa", "split.png"),
                             ("comprimi", "compress.png"), ("ruota", "rotate.png")]:
        bianca, nera = carica_icona_bicolore(f"assets/icons/{file_icona}")
        icone_bianche[nome] = bianca
        icone_nere[nome] = nera

    icona_rimuovi = carica_icona_singola("assets/icons/remove.png", (170, 170, 170))
    
    # ------------------- SIDEBAR -------------------
    sidebar_frame = ctk.CTkFrame(app, width=220, corner_radius=0)
    sidebar_frame.grid(row=0, column=0, sticky="nsw", padx=(0, 5), pady=0)

    # Icona caricata come CTkImage: gestisce automaticamente schermi a diversa densità di pixel
    icona_app = CTkImage(light_image=Image.open("assets/icona_pdforge_256.png"),
                          dark_image=Image.open("assets/icona_pdforge_256.png"),
                          size=(32, 32))

    frame_titolo = ctk.CTkFrame(sidebar_frame, fg_color="transparent")
    frame_titolo.pack(pady=(20, 5), padx=20)

    icona_titolo = ctk.CTkLabel(frame_titolo, image=icona_app, text="")
    icona_titolo.pack(side="left", padx=(0, 8))

    testo_titolo = ctk.CTkLabel(frame_titolo, text="PDForge", font=("Arial", 20, "bold"))
    testo_titolo.pack(side="left")

    sottotitolo = ctk.CTkLabel(sidebar_frame, text="Scegli un'operazione", text_color="gray")
    sottotitolo.pack(pady=(0, 15), padx=20)

    btn_unisci = ctk.CTkButton(sidebar_frame, text="   Unisci PDF", compound="left", anchor="w", image=icone_bianche["unisci"], command=azione_unisci, width=180, height=45, fg_color="transparent", border_width=2, border_color="white", text_color="white", hover_color="#444444")
    btn_unisci.pack(pady=6, padx=20)

    btn_separa = ctk.CTkButton(sidebar_frame, text="   Separa PDF", compound="left", anchor="w", image=icone_bianche["separa"], command=azione_separa, width=180, height=45, fg_color="transparent", border_width=2, border_color="white", text_color="white", hover_color="#444444")
    btn_separa.pack(pady=6, padx=20)

    btn_comprimi = ctk.CTkButton(sidebar_frame, text="   Comprimi PDF", compound="left", anchor="w", image=icone_bianche["comprimi"], command=azione_comprimi, width=180, height=45, fg_color="transparent", border_width=2, border_color="white", text_color="white", hover_color="#444444")
    btn_comprimi.pack(pady=6, padx=20)

    btn_ruota = ctk.CTkButton(sidebar_frame, text="  Ruota pagine", compound="left", anchor="w", image=icone_bianche["ruota"], command=azione_ruota, width=180, height=45, fg_color="transparent", border_width=2, border_color="white", text_color="white", hover_color="#444444")
    btn_ruota.pack(pady=6, padx=20)

    # Blocco controlli qualità compressione (nascosto finché non scegli "Comprimi PDF")
    frame_controlli_qualita = ctk.CTkFrame(sidebar_frame, fg_color="transparent")

    label_qualita = ctk.CTkLabel(frame_controlli_qualita, text="Qualità compressione: 50")
    label_qualita.pack(pady=(0, 0), padx=0)

    slider_qualita = ctk.CTkSlider(
        frame_controlli_qualita,
        from_=10,
        to=95,
        number_of_steps=17,
        command=lambda valore: aggiorna_qualita_e_label(valore, label_qualita)
    )
    slider_qualita.set(50)
    slider_qualita.pack(pady=(5, 0), padx=0, fill="x")

    # Blocco controllo angolo rotazione (nascosto finché non scegli "Ruota pagine")
    frame_controlli_angolo = ctk.CTkFrame(sidebar_frame, fg_color="transparent")

    label_angolo = ctk.CTkLabel(frame_controlli_angolo, text="Angolo di rotazione:")
    label_angolo.pack(pady=(0, 5), padx=0)

    menu_angolo = ctk.CTkOptionMenu(frame_controlli_angolo, values=["90", "180", "270"], variable=angolo_scelto)
    menu_angolo.pack(pady=(0, 0), padx=0)

    # Nessuno dei due è "impacchettato" qui: appariranno solo quando scegli l'operazione giusta

    # ------------------- AREA PRINCIPALE -------------------
    main_frame = ctk.CTkFrame(app, fg_color="transparent")
    main_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
    main_frame.grid_rowconfigure(1, weight=1)  # la lista file si espande
    main_frame.grid_columnconfigure(0, weight=1)

    label_lista = ctk.CTkLabel(main_frame, text="File selezionati", font=("Arial", 14))
    label_lista.grid(row=0, column=0, sticky="w", pady=(0, 10))

    frame_lista = ctk.CTkScrollableFrame(main_frame)
    frame_lista.grid(row=1, column=0, sticky="nsew")

    label_placeholder = ctk.CTkLabel(frame_lista, text="Nessun file selezionato", text_color="gray")
    label_placeholder.pack(anchor="w", padx=10, pady=(10, 10))

    frame_azioni = ctk.CTkFrame(main_frame, fg_color="transparent")
    frame_azioni.grid(row=2, column=0, pady=(15, 0))

    btn_aggiungi = ctk.CTkButton(frame_azioni, text="Aggiungi file", width=150, command=aggiungi_file)
    btn_aggiungi.pack(side="left", padx=10)

    btn_esegui = ctk.CTkButton(frame_azioni, text="Esegui", width=150, command=esegui)
    btn_esegui.pack(side="left", padx=10)

    # ------------------- FOOTER -------------------
    footer = ctk.CTkFrame(app, height=30, fg_color="transparent")
    footer.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 8))

    label_autore = ctk.CTkLabel(
        footer,
        text="PDForge — Fabio Di Terlizzi",
        font=("Arial", 11),
        text_color="gray"
    )
    label_autore.pack(side="left")

    # Email (sarà il più a destra)
    label_email = ctk.CTkLabel(
        footer,
        text="fabio.diterlizzi@gmail.com",
        font=("Arial", 11, "underline"),
        text_color="#6b9dc2",
        cursor="hand2"
    )
    label_email.pack(side="right")
    label_email.bind("<Button-1>", lambda evento: webbrowser.open("mailto:fabio.diterlizzi@gmail.com"))

    # Separatore tra i due link
    label_separatore = ctk.CTkLabel(
        footer,
        text="•",
        font=("Arial", 11),
        text_color="gray"
    )
    label_separatore.pack(side="right", padx=8)

    # GitHub (finirà alla sinistra del separatore)
    label_github = ctk.CTkLabel(
        footer,
        text="GitHub",
        font=("Arial", 11, "underline"),
        text_color="#6b9dc2",
        cursor="hand2"
    )
    label_github.pack(side="right")
    label_github.bind("<Button-1>", lambda evento: webbrowser.open("https://github.com/biets/PDForge"))

    app.mainloop()

# è il pattern standard per far partire il programma solo se viene eseguito direttamente, e non se viene importato come modulo
if __name__ == "__main__":
    avvia_gui()