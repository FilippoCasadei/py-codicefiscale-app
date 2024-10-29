import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from codice_fiscale import (genera_codice_fiscale, valida_cognome, valida_nome,
                            valida_sesso, valida_data_nascita, valida_comune)
from source.codice_fiscale import is_valido_codice_fiscale


def genera_codice():
    """Genera il codice fiscale basato sui dati dell'interfaccia grafica."""
    try:
        cognome = valida_cognome(entry_cognome.get())
        nome = valida_nome(entry_nome.get())
        sesso = "M" if combo_sesso.get() == "Maschio" else "F"
        giorno = combo_giorno.get().zfill(2)
        mese = combo_mese.get().zfill(2)
        anno = combo_anno.get()
        data_nascita = f"{giorno}/{mese}/{anno}"
        valida_data_nascita(data_nascita)
        comune = valida_comune(entry_comune.get())
        codice_fiscale = genera_codice_fiscale(
            cognome=cognome,
            nome=nome,
            sesso=sesso,
            data_nascita=data_nascita,
            comune=comune
        )
        label_codice_fiscale.pack(anchor="w", padx=10)
        entry_output.configure(state="normal")
        entry_output.delete(0, ctk.END)
        entry_output.insert(0, codice_fiscale)
        entry_output.pack(pady=10, padx=10, fill="x")
        entry_output.configure(state="readonly")
    except ValueError as e:
        messagebox.showerror("Errore di validazione", str(e))


def valida_codice():
    """Valida il codice fiscale inserito dall'utente."""
    codice_fiscale = entry_codice_validazione.get().upper()
    try:
        is_valido_codice_fiscale(codice_fiscale)
        messagebox.showinfo("Risultato Validazione", "Codice Fiscale VALIDO")
    except ValueError as e:
        messagebox.showerror("Risultato Validazione", f"Codice Fiscale NON VALIDO: {e}")


def switch_to_generazione():
    """Attiva la modalità di generazione codice fiscale."""
    frame_validazione.pack_forget()
    frame_generazione.pack(pady=10, padx=10, fill="x")


def switch_to_validazione():
    """Attiva la modalità di validazione codice fiscale."""
    frame_generazione.pack_forget()
    frame_validazione.pack(pady=10, padx=10, fill="x")


def avvia_gui():
    """Configura e avvia l'interfaccia grafica."""
    global entry_cognome, entry_nome, combo_sesso, combo_giorno, combo_mese, combo_anno
    global entry_comune, entry_output, label_codice_fiscale, entry_codice_validazione
    global frame_generazione, frame_validazione

    # Configurazione finestra principale
    ctk.set_appearance_mode("System")
    root = ctk.CTk()
    root.title("Codice Fiscale Tool")
    root.geometry("500x700")
    root.configure(bg="#F5F5F5")

    # Frame principale per i widget
    main_frame = ctk.CTkFrame(root, corner_radius=15, fg_color="#F0F0F0")
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Titolo
    title_label = ctk.CTkLabel(main_frame, text="GENERATORE DI CODICE FISCALE", font=("Helvetica", 18, "bold"), text_color="#333333")
    title_label.pack(pady=(10, 20))

    # Pulsanti per selezione modalità
    button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    button_frame.pack(pady=(0, 20))  # Centrato sotto il titolo

    btn_generazione = ctk.CTkButton(button_frame, text="Genera Codice Fiscale", command=switch_to_generazione, fg_color="#4CAF50")
    btn_generazione.grid(row=0, column=0, padx=10)

    btn_validazione = ctk.CTkButton(button_frame, text="Valida Codice Fiscale", command=switch_to_validazione, fg_color="#4CAF50")
    btn_validazione.grid(row=0, column=1, padx=10)

    # Frame per la modalità Generazione Codice Fiscale
    frame_generazione = ctk.CTkFrame(main_frame, fg_color="transparent")

    label_cognome = ctk.CTkLabel(frame_generazione, text="COGNOME", font=("Helvetica", 12, "bold"), text_color="#333333")
    label_cognome.pack(anchor="w", padx=10)
    entry_cognome = ctk.CTkEntry(frame_generazione, placeholder_text="Inserisci il cognome", font=("Helvetica", 12))
    entry_cognome.pack(pady=5, padx=10, fill="x")

    label_nome = ctk.CTkLabel(frame_generazione, text="NOME", font=("Helvetica", 12, "bold"), text_color="#333333")
    label_nome.pack(anchor="w", padx=10)
    entry_nome = ctk.CTkEntry(frame_generazione, placeholder_text="Inserisci il nome", font=("Helvetica", 12))
    entry_nome.pack(pady=5, padx=10, fill="x")

    label_sesso = ctk.CTkLabel(frame_generazione, text="SESSO", font=("Helvetica", 12, "bold"), text_color="#333333")
    label_sesso.pack(anchor="w", padx=10)
    combo_sesso = ctk.CTkComboBox(frame_generazione, values=["Maschio", "Femmina"], font=("Helvetica", 12))
    combo_sesso.set("Maschio")
    combo_sesso.pack(pady=5, padx=10, fill="x")

    date_frame = ctk.CTkFrame(frame_generazione, fg_color="transparent")
    date_frame.pack(pady=10, padx=10, fill="x")

    label_data = ctk.CTkLabel(date_frame, text="DATA DI NASCITA", font=("Helvetica", 12, "bold"), text_color="#333333")
    label_data.grid(row=0, column=0, columnspan=3, pady=(0, 5), sticky="w")

    giorni = [str(i).zfill(2) for i in range(1, 32)]
    combo_giorno = ctk.CTkComboBox(date_frame, values=giorni, font=("Helvetica", 12), width=60)
    combo_giorno.grid(row=1, column=0, padx=5)

    mesi = [str(i).zfill(2) for i in range(1, 13)]
    combo_mese = ctk.CTkComboBox(date_frame, values=mesi, font=("Helvetica", 12), width=60)
    combo_mese.grid(row=1, column=1, padx=5)

    current_year = datetime.now().year
    anni = [str(i) for i in range(1900, current_year + 1)]
    combo_anno = ctk.CTkComboBox(date_frame, values=anni, font=("Helvetica", 12), width=80)
    combo_anno.grid(row=1, column=2, padx=5)

    label_comune = ctk.CTkLabel(frame_generazione, text="LUOGO DI NASCITA", font=("Helvetica", 12, "bold"), text_color="#333333")
    label_comune.pack(anchor="w", padx=10)
    entry_comune = ctk.CTkEntry(frame_generazione, placeholder_text="Inserisci il comune", font=("Helvetica", 12))
    entry_comune.pack(pady=5, padx=10, fill="x")

    btn_generare = ctk.CTkButton(frame_generazione, text="Genera Codice Fiscale", command=genera_codice, fg_color="#4CAF50", font=("Helvetica", 12, "bold"))
    btn_generare.pack(pady=20)

    label_codice_fiscale = ctk.CTkLabel(frame_generazione, text="CODICE FISCALE", font=("Helvetica", 12, "bold"), text_color="#333333")
    entry_output = ctk.CTkEntry(frame_generazione, font=("Helvetica", 12, "bold"), state="readonly")

    # Frame per la modalità Validazione Codice Fiscale
    frame_validazione = ctk.CTkFrame(main_frame, fg_color="transparent")

    label_validazione = ctk.CTkLabel(frame_validazione, text="INSERISCI CODICE FISCALE", font=("Helvetica", 12, "bold"), text_color="#333333")
    label_validazione.pack(anchor="w", padx=10)
    entry_codice_validazione = ctk.CTkEntry(frame_validazione, placeholder_text="Inserisci codice fiscale", font=("Helvetica", 12))
    entry_codice_validazione.pack(pady=5, padx=10, fill="x")

    btn_valida = ctk.CTkButton(frame_validazione, text="Valida Codice Fiscale", command=valida_codice, fg_color="#4CAF50", font=("Helvetica", 12, "bold"))
    btn_valida.pack(pady=20)

    switch_to_generazione()

    root.mainloop()


if __name__ == "__main__":
    avvia_gui()
