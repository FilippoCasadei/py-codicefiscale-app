import tkinter as tk
from tkinter import messagebox, font, ttk
from tkcalendar import Calendar
from codice_fiscale import (genera_codice_fiscale, valida_cognome, valida_nome,
                            valida_sesso, valida_data_nascita, valida_comune)

def genera_codice():
    """Genera il codice fiscale basato sui dati dell'interfaccia grafica."""
    try:
        cognome = valida_cognome(entry_cognome.get())
        nome = valida_nome(entry_nome.get())
        sesso = valida_sesso(combo_sesso.get())
        data_nascita = calendar.get_date()
        comune = valida_comune(entry_comune.get())

        codice_fiscale = genera_codice_fiscale(
            cognome=cognome,
            nome=nome,
            sesso=sesso,
            data_nascita=data_nascita,
            comune=comune
        )
        label_output.config(text=f"Codice Fiscale: {codice_fiscale}", fg="#4CAF50")
    except ValueError as e:
        messagebox.showerror("Errore di validazione", str(e))


def avvia_gui():
    """Configura e avvia l'interfaccia grafica."""
    global entry_cognome, entry_nome, combo_sesso, calendar, entry_comune, label_output

    # Configurazione della finestra principale
    root = tk.Tk()
    root.title("Generatore di Codice Fiscale")
    root.geometry("500x450")  # Dimensione aumentata
    root.state("zoomed")  # Apertura a schermo intero
    root.configure(bg="#F5F5F5")  # Sfondo chiaro

    # Font personalizzati
    titolo_font = font.Font(family="Helvetica", size=16, weight="bold")
    label_font = font.Font(family="Helvetica", size=10)
    entry_font = font.Font(family="Helvetica", size=10)

    # Frame centrale per i widget
    main_frame = tk.Frame(root, bg="#F5F5F5", padx=20, pady=20)
    main_frame.pack(expand=True)

    # Titolo
    tk.Label(main_frame, text="Generatore di Codice Fiscale", font=titolo_font, bg="#F5F5F5", fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 15))

    # Campi di input con etichette
    tk.Label(main_frame, text="Cognome:", font=label_font, bg="#F5F5F5").grid(row=1, column=0, sticky="e", pady=5)
    entry_cognome = tk.Entry(main_frame, font=entry_font, width=25)
    entry_cognome.grid(row=1, column=1, pady=5)

    tk.Label(main_frame, text="Nome:", font=label_font, bg="#F5F5F5").grid(row=2, column=0, sticky="e", pady=5)
    entry_nome = tk.Entry(main_frame, font=entry_font, width=25)
    entry_nome.grid(row=2, column=1, pady=5)

    # Combobox per la scelta del sesso
    tk.Label(main_frame, text="Sesso:", font=label_font, bg="#F5F5F5").grid(row=3, column=0, sticky="e", pady=5)
    combo_sesso = ttk.Combobox(main_frame, values=["M", "F"], font=entry_font, width=23, state="readonly")
    combo_sesso.grid(row=3, column=1, pady=5)
    combo_sesso.set("M")  # Imposta il valore predefinito

    # Calendario per la scelta della data di nascita
    tk.Label(main_frame, text="Data di nascita:", font=label_font, bg="#F5F5F5").grid(row=4, column=0, sticky="e", pady=5)
    calendar = Calendar(main_frame, date_pattern="dd/mm/yyyy", font=entry_font)
    calendar.grid(row=4, column=1, pady=5)

    # Campo di input per il comune
    tk.Label(main_frame, text="Comune o Stato di nascita:", font=label_font, bg="#F5F5F5").grid(row=5, column=0, sticky="e", pady=5)
    entry_comune = tk.Entry(main_frame, font=entry_font, width=25)
    entry_comune.grid(row=5, column=1, pady=5)

    # Bottone per generare il codice fiscale
    btn_generare = tk.Button(main_frame, text="Genera Codice Fiscale", command=genera_codice, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"), padx=10, pady=5)
    btn_generare.grid(row=6, column=0, columnspan=2, pady=15)

    # Etichetta per l'output del codice fiscale generato
    label_output = tk.Label(main_frame, text="", bg="#F5F5F5", font=("Helvetica", 10, "italic"))
    label_output.grid(row=7, column=0, columnspan=2, pady=(10, 0))

    root.mainloop()
