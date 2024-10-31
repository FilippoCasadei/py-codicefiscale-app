# Generatore di Codice Fiscale

Questo progetto è un generatore di codice fiscale basato sui dati anagrafici italiani. Utilizza una GUI costruita con `CustomTkinter` e una libreria per generare e validare codici fiscali.

## Funzionalità
- **Generazione del codice fiscale**: Genera il codice fiscale italiano basato su nome, cognome, data di nascita, sesso e comune/stato di nascita.
- **Validazione del codice fiscale**: Verifica se un codice fiscale inserito ha un formato corretto e valido.
- **Interfaccia Grafica**: Offre un'interfaccia utente moderna e interattiva grazie a `CustomTkinter`.

## Requisiti
- Python 3.7 o superiore
- `tkinter`
- `customtkinter`
- `tkcalendar`
- `pytest` (per eseguire i test)
- `pytest-cov` (per generare report di copertura dei test)

## Installazione
1. Clona il repository:
    ```bash
    git clone <url-del-repository>
    cd <nome-cartella-progetto>
    ```

2. Installa le dipendenze:
    ```bash
    pip install customtkinter tkcalendar pytest pytest-cov
    ```


3. Esegui l'applicazione:
     ```bash
     python main.py
     ```

## Esecuzione dei Test
Per eseguire i test e verificare che tutte le funzionalità funzionino correttamente, utilizza il comando:
```bash
pytest

pytest --cov=. --cov-report=term-missing  # report sulla copertura dei test
pytest --cov=. --cov-report=html          # report in formato HTML
```


## Struttura del progetto
```bash
project_folder/
├── source/                          # Moduli sorgente del progetto
│   ├── __init__.py
│   ├── main.py                      # Punto di ingresso per l'app GUI
│   ├── README.md                    # Documentazione del progetto
│   ├── tests/                       # Test unitari per le funzionalità del progetto
│   │   ├── __init__.py
│   │   ├── test_codice_fiscale.py   # Test per le funzioni di codifica del codice fiscale
│   │   └── test_funzioni_validazione.py  # Test per le funzioni di validazione del codice fiscale
│   └── data/      
│       ├── tabella_comuni.csv       # Elenco dei comuni e dei loro codici catastali
│       └── tabella_stati.csv        # Elenco degli stati esteri e dei loro codici catastali
```

## Esempio di Utilizzo
- Avvia l'applicazione eseguendo main.py.
- Scegli la modalità tra le 3 proposte:
  - g: utilizza la GUI
  - c: utilizza la linea di comando
    - g: genera un codice fiscale
    - v: valida un codice fiscale
  - q: termina il programma
