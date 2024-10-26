import csv

def crea_dict_denominazione_codice_nazionale_da_csv(file_path: str) -> dict[str: str]:
    dizionario_codici = {}
    with open(file_path, mode='r', encoding='latin1') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            denominazione = row.get("Denominazione Italiana").upper()
            codice_catastale = row.get("Codice Nazionale")
            if denominazione and codice_catastale:  # Salta le righe incomplete
                dizionario_codici[denominazione] = codice_catastale
    return dizionario_codici

comuni = crea_dict_denominazione_codice_nazionale_da_csv('data/tabella_comuni.csv')
stati = crea_dict_denominazione_codice_nazionale_da_csv('data/tabella_stati.csv')
print(comuni)
print(stati)