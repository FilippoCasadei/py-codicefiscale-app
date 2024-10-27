from codice_fiscale import CodiceFiscale

def build_codice_fiscale() -> CodiceFiscale:
    cognome = input("Inserisci il cognome: ")
    nome = input("Inserisci il nome: ")
    sesso = input("Inserisci il sesso ('m' o 'f'): ")
    data = input("Inserisci la data di nascita ('DD/MM/YYYY'): ")
    comune = input("Inserisci il comune o stato estero di nascita: ")

    return CodiceFiscale(cognome, nome, sesso, data, comune)

def main():
    while True:
        scelta = input("Premi invio per generare il codice fiscale, 'q' per terminare il programma:")
        if scelta == "":
            persona = build_codice_fiscale()
            codice_fiscale_persona = persona.genera_codice_fiscale()
            print(codice_fiscale_persona)
        else:
            break

main()


