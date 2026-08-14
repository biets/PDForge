import customtkinter as ctk
from tkinter import filedialog, messagebox  # messagebox per avvisi ed errori
from pypdf import PdfReader

file_selezionati = []
operazione_scelta = None
valore_qualita = 50  # valore di default della compressione

# Variabile per tenere traccia dell'angolo scelto (default 90°)
angolo_scelto = None  # verrà creata come StringVar dentro avvia_gui(), dopo la creazione della finestra

def azione_unisci():
    global operazione_scelta
    operazione_scelta = "unisci"
    print("Operazione selezionata: Unisci PDF")

def azione_separa():
    global operazione_scelta
    operazione_scelta = "separa"
    print("Operazione selezionata: Separa PDF")

def azione_comprimi():
    global operazione_scelta
    operazione_scelta = "comprimi"
    print("Operazione selezionata: Comprimi PDF")

def azione_ruota():
    global operazione_scelta
    operazione_scelta = "ruota"
    print("Operazione selezionata: Ruota pagine")



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
        angolo = int(angolo_scelto.get())

        cartella_output = filedialog.askdirectory(title="Scegli la cartella dove salvare i PDF ruotati")
        if cartella_output == "":
            return

        try:
            for percorso_file in file_selezionati:
                nome_file = percorso_file.split("/")[-1]
                nome_output = nome_file.replace(".pdf", "_ruotato.pdf")
                percorso_output = f"{cartella_output}/{nome_output}"
                rotate_pdf(percorso_file, angolo, percorso_output)

            file_selezionati.clear()
            aggiorna_lista_visiva()
            messagebox.showinfo("Completato", "PDF ruotati con successo!")
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

def aggiorna_lista_visiva():
    # Puliamo il frame prima di ridisegnare (altrimenti si accumulano le label vecchie)
    for widget in frame_lista.winfo_children():
        widget.destroy()

    if len(file_selezionati) == 0:
        label = ctk.CTkLabel(frame_lista, text="Nessun file selezionato", text_color="gray")
        label.pack(anchor="w", padx=10, pady=(10, 10))
    else:
        for percorso in file_selezionati:
            # Mostriamo solo il nome del file, non tutto il percorso completo
            nome_file = percorso.split("/")[-1]
            label = ctk.CTkLabel(frame_lista, text=nome_file)
            label.pack(anchor="w", padx=10, pady=2)

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
    global frame_lista, angolo_scelto # entrmabe vanno dichiarate global

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("PDForge")
    app.geometry("600x400")

    # Ora che la finestra esiste, possiamo creare la StringVar
    angolo_scelto = ctk.StringVar(value="90")

    # Pulsanti per le operazioni principali

    titolo = ctk.CTkLabel(app, text="Scegli un'operazione", font=("Arial", 16))
    titolo.grid(row=0, column=0, columnspan=2, pady=(20, 10))

    btn_unisci = ctk.CTkButton(app, text="Unisci PDF", command=azione_unisci, width=200, height=60)
    btn_unisci.grid(row=1, column=0, padx=10, pady=10)

    btn_separa = ctk.CTkButton(app, text="Separa PDF", command=azione_separa, width=200, height=60)
    btn_separa.grid(row=1, column=1, padx=10, pady=10)

    btn_comprimi = ctk.CTkButton(app, text="Comprimi PDF", command=azione_comprimi, width=200, height=60)
    btn_comprimi.grid(row=2, column=0, padx=10, pady=10)

    btn_ruota = ctk.CTkButton(app, text="Ruota pagine", command=azione_ruota, width=200, height=60)
    btn_ruota.grid(row=2, column=1, padx=10, pady=10)

    #slider per la qualità della compressione
    label_qualita = ctk.CTkLabel(app, text="Qualità compressione: 50")
    label_qualita.grid(row=3, column=0, columnspan=2, pady=(10, 0))

    slider_qualita = ctk.CTkSlider(
        app,
        from_=10,
        to=95,
        number_of_steps=17,
        command=lambda valore: aggiorna_qualita_e_label(valore, label_qualita)
    )
    slider_qualita.set(50)
    slider_qualita.grid(row=4, column=0, columnspan=2, pady=(0, 10), sticky="ew", padx=20)

    # Etichetta e menu a tendina per la scelta dell'angolo di rotazione
    label_angolo = ctk.CTkLabel(app, text="Angolo di rotazione:")
    label_angolo.grid(row=5, column=0, pady=(10, 0), sticky="e")

    menu_angolo = ctk.CTkOptionMenu(
        app,
        values=["90", "180", "270"],
        variable=angolo_scelto
    )
    menu_angolo.grid(row=5, column=1, pady=(10, 0), sticky="w")


    frame_lista = ctk.CTkScrollableFrame(app, height=100)
    frame_lista.grid(row=6, column=0, columnspan=2, padx=10, pady=(20, 10), sticky="nsew")

    label_placeholder = ctk.CTkLabel(frame_lista, text="Nessun file selezionato", text_color="gray")
    label_placeholder.pack(anchor="w", padx=10, pady=(10, 10))

    frame_azioni = ctk.CTkFrame(app, fg_color="transparent")
    frame_azioni.grid(row=7, column=0, columnspan=2, pady=20)

    btn_aggiungi = ctk.CTkButton(frame_azioni, text="Aggiungi file", width=150, command=aggiungi_file)
    btn_aggiungi.pack(side="left", padx=10)

    btn_esegui = ctk.CTkButton(frame_azioni, text="Esegui", width=150, command=esegui)
    btn_esegui.pack(side="left", padx=10)

    app.mainloop()

# è il pattern standard per far partire il programma solo se viene eseguito direttamente, e non se viene importato come modulo
if __name__ == "__main__":
    avvia_gui()