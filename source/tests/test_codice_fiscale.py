import pytest
from source.codice_fiscale import *

# COSA FARE?
# FINIRE I TEST
# DEFINIRE BENE PERCORSI RELATIVI (SI POTREBBE USARE os)
# tests/test_codifica.py


#######################################
# TEST PER GENERAZIONE CODICE FISCALE #
#######################################
@pytest.mark.parametrize("cognome, nome, sesso, data_nascita, comune, expected", [
    ("Rossi", "Mario", "M", "01/01/1985", "Roma", "RSSMRA85M01H501Z"),    # Caso standard maschile
    ("Martini", "Mattia", "M", "09/04/1925", "Milano", "MRTMTT25D09F205B"), # Caso standard maschile con data diversa
    ("Bianchi", "Lara", "F", "20/11/1998", "Milano", "BLTTLR98S20F205X"),  # Caso standard femminile
    ("Giorgi", "Maria", "M", "10/08/1985", "Lecce", "GRGMRA85M10L219C"),   # Caso maschile con comune diverso
])
def test_genera_codice_fiscale(cognome, nome, sesso, data_nascita, comune, expected):
    assert genera_codice_fiscale(cognome, nome, sesso, data_nascita, comune) == expected


#############################
# TEST PER CODIFICA COGNOME #
#############################
@pytest.mark.parametrize("cognome, expected", [
    ("Rossi", "RSS"),              # Cognome con 3 consonanti
    ("Di Giovanni", "DGV"),        # Cognome con spazio, estrazione consonanti
    ("Le", "LEX"),                 # Cognome breve, aggiunta di 'X'
    ("Ai", "AIX"),                 # Cognome di sole vocali
    ("O'Connor", "CNN")            # Cognome con apostrofo, ignorato
])
def test_codifica_cognome(cognome, expected):
    assert codifica_cognome(cognome) == expected


##########################
# TEST PER CODIFICA NOME #
##########################
@pytest.mark.parametrize("nome, expected", [
    ("Marco", "MRC"),              # Nome con 3 consonanti
    ("Giuseppe", "GPP"),           # Nome con più di 3 consonanti (si salta la seconda)
    ("Elena", "LNE"),              # Nome con meno di 3 consonanti
    ("Ai", "AIX"),                 # Nome breve di sole vocali, aggiunta di 'X'
    ("Jean-Claude", "JCL")         # Nome con trattino, ignorato
])
def test_codifica_nome(nome, expected):
    assert codifica_nome(nome) == expected


#####################################
# TEST PER CODIFICA DATA DI NASCITA #
#####################################
@pytest.mark.parametrize("data_nascita, sesso, expected", [
    ("01/01/2000", "M", "00A01"),  # Uomo, data normale
    ("01/01/2000", "F", "00A41"),  # Donna, +40 sul giorno
    ("15/07/1995", "M", "95L15"),  # Uomo, mese luglio
    ("10/10/1980", "F", "80R50"),  # Donna, giorno 10 -> 50
    ("29/02/2020", "M", "20B29")   # Uomo, anno bisestile
])
def test_codifica_data_nascita(data_nascita, sesso, expected):
    assert codifica_data_nascita(data_nascita, sesso) == expected


############################
# TEST PER CODIFICA COMUNE #
############################
@pytest.mark.parametrize("comune, expected", [
    ("ROMA", "H501"),             # Codice nazionale per Roma
    ("Milano", "F205"),           # Codice nazionale per Milano
    ("Napoli", "F839"),           # Codice nazionale per Napoli
    ("ALBANIA", "Z100"),          # Codice nazionale per Albania
    ("irlanda", "Z116")           # Codice nazionale per Irlanda
])
def test_codifica_comune(comune, expected):
    assert codifica_comune(comune) == expected


###########################################
# TEST PER CALCOLO CARATTERE DI CONTROLLO #
###########################################
@pytest.mark.parametrize("codice_senza_controllo, expected", [
    ("RSSMRA85M01H501", "Z"),  # Codice parziale per "Rossi Mario", maschio, 01/01/1985, Roma
    ("MRTMTT25D09F205", "B"),  # Codice parziale per "Martini Mattia", maschio, 09/04/1925, Milano
    ("BLTTLR98S20F205", "X"),  # Codice parziale per "Bianchi Lara", femmina, 20/11/1998, Milano
    ("GRGMRA85M10L219", "C"),  # Codice parziale per "Giorgi Maria", maschio, 10/08/1985, Lecce
])
def test_calcola_carattere_controllo(codice_senza_controllo, expected):
    assert calcola_carattere_controllo(codice_senza_controllo) == expected