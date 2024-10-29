# tests/test_funzioni_validazione.py

import pytest
from datetime import datetime, timedelta
from source.codice_fiscale import is_valido_codice_fiscale, valida_cognome, valida_nome, valida_sesso, valida_data_nascita, valida_comune


#######################################
# TEST PER VALIDAZIONE CODICE FISCALE #
#######################################
@pytest.mark.parametrize("codice_fiscale", [
    "RSSMRA85A01H501Z",  # Codice fiscale corretto 1 "Rossi", "Mario", "M", "01/01/1985", "Roma"
    "CLDSCH69D55H294C",  # Codice fiscale corretto 2 "Claudia", "Sanchi", "F", "15/04/1969", "Rimini"
    "CRSRLD00A01F205F",  # Codice fiscale corretto 3 "Cristiano", "Ronaldo", "M", "01/01/2000", "Milano"
])
def test_is_valido_codice_fiscale_valido(codice_fiscale):
    """Testa codici fiscali validi per verificare che la funzione ritorni True."""
    assert is_valido_codice_fiscale(codice_fiscale) is True


@pytest.mark.parametrize("codice_fiscale, expected_error", [
    ("RSSMRA85M01H50", "Codice fiscale non valido. Deve essere lungo 16 caratteri."), # Lunghezza errata
    ("R8SMRA85M01H501Z", "Codice fiscale non valido. Posizioni 1-3 devono essere lettere per cognome"), # Posizione 1-3 'R8S' non lettere
    ("RSSM8A85M01H501Z", "Codice fiscale non valido. Posizioni 4-6 devono essere lettere per nome"), # Posizione 4-6 'M8A' non lettere
    ("RSSMRA8AM01H501Z", "Codice fiscale non valido. Posizioni 7-8 devono essere numeri per anno"), # Posizione 7-8 '8A' non numeri
    ("RSSMRA85101H501Z", "Codice fiscale non valido. Posizione 9 deve essere una lettere per mese"), # Posizione 9 '1' non lettera
    ("RSSMRA85M99H501Z", "Codice fiscale non valido. Posizioni 10-11 devono rappresentare un numero tra 01 e 71"), # Posizione 10-11 '99' fuori range
    ("RSSMRA85M01X501Z", "Codice fiscale non valido. Posizioni 12-15 devono rappresentare un valido codice catastale"), # 'X510' non è un codice catastale
    ("RSSMRA85M01H501A", "Codice fiscale non valido. Il carattere di controllo non corrisponde.") # Carattere di controllo 'A' non valido
])
def test_is_valido_codice_fiscale_non_valido(codice_fiscale, expected_error):
    """Testa codici fiscali non validi per verificare che venga sollevato l'errore corretto."""
    with pytest.raises(ValueError) as excinfo:
        is_valido_codice_fiscale(codice_fiscale)
    assert str(excinfo.value).startswith(expected_error)


################################
# TEST PER VALIDAZIONE COGNOMI #
################################
@pytest.mark.parametrize("cognome, expected", [
    ("Rossi", "ROSSI"),
    (" Di Giovanni ", "DIGIOVANNI"),
    ("D'Angelo", "D'ANGELO"),
    ("Müller", "MULLER"),
    ("Smith-Jones", "SMITH-JONES"),
])
def test_valida_cognome_valido(cognome, expected):
    assert valida_cognome(cognome) == expected


@pytest.mark.parametrize("cognome", [
    "", "A", "Rossi!", "@" * 3, "Z" * 51
])
def test_valida_cognome_non_valido(cognome):
    with pytest.raises(ValueError, match="Cognome non valido"):
        valida_cognome(cognome)


#############################
# TEST PER VALIDAZIONE NOMI #
#############################
@pytest.mark.parametrize("nome, expected", [
    ("Luca", "LUCA"),
    (" D'Alessandro ", "D'ALESSANDRO"),
    ("José", "JOSE"),
    ("Anna Maria", "ANNAMARIA"),
    ("Jean-Claude", "JEAN-CLAUDE"),
])
def test_valida_nome_valido(nome, expected):
    assert valida_nome(nome) == expected


@pytest.mark.parametrize("nome", [
    "", "A", "Anna@Maria", "!" * 3, "A" * 51
])
def test_valida_nome_non_valido(nome):
    with pytest.raises(ValueError, match="Nome non valido"):
        valida_nome(nome)


##############################
# TEST PER VALIDAZIONE SESSO #
##############################
@pytest.mark.parametrize("sesso, expected", [
    ("M", "M"),
    ("m", "M"),
    ("F", "F"),
    ("f", "F"),
])
def test_valida_sesso_valido(sesso, expected):
    assert valida_sesso(sesso) == expected


@pytest.mark.parametrize("sesso", [
    "X", "Male", "Femminile", ""
])
def test_valida_sesso_non_valido(sesso):
    with pytest.raises(ValueError, match="Sesso non valido"):
        valida_sesso(sesso)


########################################
# TEST PER VALIDAZIONE DATA DI NASCITA #
########################################
@pytest.mark.parametrize("data_nascita, expected", [
    ("01/01/2000", "01/01/2000"),
    ("29/02/2020", "29/02/2020"),
    ((datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y"),
     (datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y")),
])
def test_valida_data_nascita_valida(data_nascita, expected):
    assert valida_data_nascita(data_nascita) == expected


@pytest.mark.parametrize("data_nascita", [
    "31/02/2000", "29/02/2050", "31/12/1899", "01-01-2000",
    (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y"), ""
])
def test_valida_data_nascita_non_valida(data_nascita):
    with pytest.raises(ValueError, match="Data di nascita non valida"):
        valida_data_nascita(data_nascita)


###############################
# TEST PER VALIDAZIONE COMUNE #
###############################
@pytest.mark.parametrize("comune", [
    "ROMA", "milano", "Napoli", "IRLANDA", "albania"
])
def test_valida_comune_valido(comune):
    assert valida_comune(comune) == comune.upper()


@pytest.mark.parametrize("comune", [
    "Atlantide", "Gotham", ""
])
def test_valida_comune_non_valido(comune):
    with pytest.raises(ValueError, match="Comune/Stato non valido"):
        valida_comune(comune)
