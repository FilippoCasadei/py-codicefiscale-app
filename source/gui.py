import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from codice_fiscale import (genera_codice_fiscale, valida_cognome, valida_nome,
                            valida_sesso, valida_data_nascita, valida_comune)


def genera_codice():
    """Genera il codice fiscale basato sui dati dell'interfaccia grafica."""
    try:
        cognome = valida_cognome(entry_cognome.get())
        nome = valida_nome(entry_nome.get())

        # Conversione del sesso selezionato
        sesso = "M" if combo_sesso.get() == "Maschio" else "F"

        # Formattazione della data
        giorno = combo_giorno.get().zfill(2)  # Formato GG
        mese = combo_mese.get().zfill(2)      # Formato MM
        anno = combo_anno.get()               # Formato AAAA
        data_nascita = f"{giorno}/{mese}/{anno}"

        # Validazione della data
        valida_data_nascita(data_nascita)

        comune = valida_comune(entry_comune.get())

        # Generazione del codice fiscale
        codice_fiscale = genera_codice_fiscale(
            cognome=cognome,
            nome=nome,
            sesso=sesso,
            data_nascita=data_nascita,
            comune=comune
        )

        # Visualizza l'etichetta e il campo di output e mostra il codice generato
        label_codice_fiscale.pack(anchor="w", padx=10)
        entry_output.configure(state="normal")
        entry_output.delete(0, ctk.END)
        entry_output.insert(0, codice_fiscale)
        entry_output.pack(pady=10, padx=10, fill="x")
        entry_output.configure(state="readonly")  # Blocca il campo dopo l'inserimento
    except ValueError as e:
        messagebox.showerror("Errore di validazione", str(e))


def avvia_gui():
    """Configura e avvia l'interfaccia grafica."""
    global entry_cognome, entry_nome, combo_sesso, combo_giorno, combo_mese, combo_anno, entry_comune, entry_output, label_codice_fiscale

    # Configurazione finestra principale
    ctk.set_appearance_mode("System")  # Tema chiaro/scuro automatico
    root = ctk.CTk()
    root.title("Generatore di Codice Fiscale")
    root.geometry("500x700")
    root.configure(bg="#F5F5F5")

    # Frame principale per i widget
    main_frame = ctk.CTkFrame(root, corner_radius=15, fg_color="#F0F0F0")
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Titolo
    title_label = ctk.CTkLabel(main_frame, text="GENERATORE DI CODICE FISCALE", font=("Helvetica", 18, "bold"), text_color="#333333")
    title_label.pack(pady=(10, 20))

    # Campo Cognome
    label_cognome = ctk.CTkLabel(main_frame, text="COGNOME", font=("Helvetica", 12, "bold"), text_color="#333333")
    label_cognome.pack(anchor="w", padx=10)
    entry_cognome = ctk.CTkEntry(main_frame, placeholder_text="Inserisci il cognome", font=("Helvetica", 12))
    entry_cognome.pack(pady=5, padx=10, fill="x")

    # Campo Nome
    label_nome = ctk.CTkLabel(main_frame, text="NOME", font=("Helvetica", 12, "bold"), text_color="#333333")
    label_nome.pack(anchor="w", padx=10)
    entry_nome = ctk.CTkEntry(main_frame, placeholder_text="Inserisci il nome", font=("Helvetica", 12))
    entry_nome.pack(pady=5, padx=10, fill="x")

    # Campo Sesso
    label_sesso = ctk.CTkLabel(main_frame, text="SESSO", font=("Helvetica", 12, "bold"), text_color="#333333")
    label_sesso.pack(anchor="w", padx=10)
    combo_sesso = ctk.CTkComboBox(main_frame, values=["Maschio", "Femmina"], font=("Helvetica", 12))
    combo_sesso.set("Maschio")
    combo_sesso.pack(pady=5, padx=10, fill="x")

    # Sezione per la data di nascita
    date_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    date_frame.pack(pady=10, padx=10, fill="x")

    label_data = ctk.CTkLabel(date_frame, text="DATA DI NASCITA", font=("Helvetica", 12, "bold"), text_color="#333333")
    label_data.grid(row=0, column=0, columnspan=3, pady=(0, 5), sticky="w")

    # ComboBox per il giorno
    giorni = [str(i).zfill(2) for i in range(1, 32)]
    combo_giorno = ctk.CTkComboBox(date_frame, values=giorni, font=("Helvetica", 12), width=60)
    combo_giorno.grid(row=1, column=0, padx=5)

    # ComboBox per il mese
    mesi = [str(i).zfill(2) for i in range(1, 13)]
    combo_mese = ctk.CTkComboBox(date_frame, values=mesi, font=("Helvetica", 12), width=60)
    combo_mese.grid(row=1, column=1, padx=5)

    # ComboBox per l'anno
    current_year = datetime.now().year
    anni = [str(i) for i in range(1900, current_year + 1)]
    combo_anno = ctk.CTkComboBox(date_frame, values=anni, font=("Helvetica", 12), width=80)
    combo_anno.grid(row=1, column=2, padx=5)

    # Campo Comune
    label_comune = ctk.CTkLabel(main_frame, text="LUOGO DI NASCITA", font=("Helvetica", 12, "bold"), text_color="#333333")
    label_comune.pack(anchor="w", padx=10)
    entry_comune = ctk.CTkEntry(main_frame, placeholder_text="Inserisci il comune", font=("Helvetica", 12))
    entry_comune.pack(pady=5, padx=10, fill="x")

    # Bottone per generare il codice fiscale
    btn_generare = ctk.CTkButton(main_frame, text="Genera Codice Fiscale", command=genera_codice, fg_color="#4CAF50", font=("Helvetica", 12, "bold"))
    btn_generare.pack(pady=20)

    # Etichetta e campo di output per il codice fiscale (inizialmente nascosti)
    label_codice_fiscale = ctk.CTkLabel(main_frame, text="CODICE FISCALE", font=("Helvetica", 12, "bold"), text_color="#333333")
    entry_output = ctk.CTkEntry(main_frame, font=("Helvetica", 12, "bold"), state="readonly")

    root.mainloop()


# Chiamare la funzione di avvio GUI solo quando esplicitamente chiamata
if __name__ == "__main__":
    avvia_gui()
