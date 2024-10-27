from codice_fiscale import genera_codice_fiscale, valida_cognome, valida_nome, valida_sesso, valida_data_nascita, valida_comune


def acquisisci_dato(messaggio_da_stampare: str, funzione_validazione) -> str:
    """Acquisisce un dato anagrafico dall'utente e lo valida.

    Chiede all'utente di inserire un dato anagrafico e lo valida usando la funzione
    di validazione fornita. Ripete la richiesta fino a quando il dato è valido.

    Args:
        messaggio_da_stampare (str): Messaggio mostrato all'utente per l'inserimento del dato.
        funzione_validazione (callable): Funzione usata per validare il dato anagrafico.

    Returns:
        str: Dato anagrafico validato.
    """
    while True:
        dato_anagrafico = input(messaggio_da_stampare)
        try:
            return funzione_validazione(dato_anagrafico)
        except ValueError as e:
            print(f"ERRORE: {e}")


def acquisisci_dati_anagrafici() -> dict:
    """Gestisce l'acquisizione e la validazione dei dati anagrafici dell'utente.

    Acquisisce i dati anagrafici dell'utente uno alla volta, utilizzando le funzioni di
    validazione associate a ciascun tipo di dato. Ogni dato viene richiesto finché non è valido.

    Returns:
        dict: Dizionario contenente i dati anagrafici validati.
    """
    mappa_validazione = {
        "cognome": ("Inserisci il cognome: ", valida_cognome),
        "nome": ("Inserisci il nome: ", valida_nome),
        "sesso": ("Inserisci il sesso ('m' o 'f'): ", valida_sesso),
        "data_nascita": ("Inserisci la data di nascita ('DD/MM/YYYY'): ", valida_data_nascita),
        "comune": ("Inserisci il comune o stato estero di nascita: ", valida_comune)
    }
    dati_anagrafici = {}
    for nome_dato_anagrafico, (messaggio_da_stampare, funzione_validazione) in mappa_validazione.items():
        dati_anagrafici[nome_dato_anagrafico] = acquisisci_dato(messaggio_da_stampare,
                                                                funzione_validazione)
    return dati_anagrafici


def main() -> None:
    """Funzione principale del programma.

    Gestisce il ciclo principale per l'inserimento dei dati e la generazione del codice fiscale.
    L'utente può scegliere di generare un nuovo codice fiscale o terminare il programma.
    """
    while True:
        scelta = input("Premi invio per generare il codice fiscale, 'q' per terminare il programma:")
        if scelta == "":
            dati_anagrafici = acquisisci_dati_anagrafici()
            codice_fiscale = genera_codice_fiscale(**dati_anagrafici)  # Unpacking del dizionario
            print(f"Codice Fiscale Generato: {codice_fiscale}")
        elif scelta.lower() == 'q':
            print("Programma terminato.")
            break
        else:
            print("Input non valido. Riprova.")


# Esegui il main solo se il file è eseguito come script principale
if __name__ == "__main__":
    main()
