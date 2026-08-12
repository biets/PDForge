import customtkinter as ctk
from tkinter import filedialog, messagebox  # messagebox per avvisi ed errori

file_selezionati = []
operazione_scelta = None  # nessuna operazione selezionata all'avvio

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
                messagebox.showinfo("Completato", "PDF uniti con successo!")
            except Exception as errore:
                messagebox.showerror("Errore", f"Qualcosa è andato storto:\n{errore}")

    else:
            # Le altre operazioni le colleghiamo nei prossimi passi
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


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("PDForge")
app.geometry("600x400")

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

frame_lista = ctk.CTkFrame(app)
frame_lista.grid(row=3, column=0, columnspan=2, padx=10, pady=(20, 10), sticky="nsew")

label_placeholder = ctk.CTkLabel(frame_lista, text="Nessun file selezionato", text_color="gray")
label_placeholder.pack(anchor="w", padx=10, pady=(10, 10))

frame_azioni = ctk.CTkFrame(app, fg_color="transparent")
frame_azioni.grid(row=4, column=0, columnspan=2, pady=20)

btn_aggiungi = ctk.CTkButton(frame_azioni, text="Aggiungi file", width=150, command=aggiungi_file)
btn_aggiungi.pack(side="left", padx=10)

btn_esegui = ctk.CTkButton(frame_azioni, text="Esegui", width=150, command=esegui)
btn_esegui.pack(side="left", padx=10)

app.mainloop()