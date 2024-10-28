# tests/test_funzioni_validazione.py

import pytest
from datetime import datetime, timedelta
from source.codice_fiscale import valida_cognome, valida_nome, valida_sesso, valida_data_nascita, valida_comune


# TEST PER VALIDAZIONE COGNOMI
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


# TEST PER VALIDAZIONE NOMI
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


# TEST PER VALIDAZIONE SESSO
@pytest.mark.parametrize("sesso, expected", [
    ("M", "M"),
    ("m", "M"),
    ("F", "F"),
    ("f", "F"),
])
def test_valida_sesso_valido(sesso, expected):
    assert valida_sesso(sesso) == expected


@pytest.mark.parametrize("sesso", [
    "X", "Male", "Femminile", "", None
])
def test_valida_sesso_non_valido(sesso):
    with pytest.raises(ValueError, match="Sesso non valido"):
        valida_sesso(sesso)


# TEST PER VALIDAZIONE DATA DI NASCITA
@pytest.mark.parametrize("data_nascita, expected", [
    ("01/01/2000", "01/01/2000"),
    ("29/02/2020", "29/02/2020"),
    ((datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y"),
     (datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y")),
])
def test_valida_data_nascita_valida(data_nascita, expected):
    assert valida_data_nascita(data_nascita) == expected


@pytest.mark.parametrize("data_nascita", [
    "31/02/2000", "29/02/2019", "01-01-2000",
    (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y"), "", None
])
def test_valida_data_nascita_non_valida(data_nascita):
    with pytest.raises(ValueError, match="Data di nascita non valida"):
        valida_data_nascita(data_nascita)


# TEST PER VALIDAZIONE COMUNE
@pytest.mark.parametrize("comune", [
    "ROMA", "milano", "Napoli", "IRLANDA", "albania"
])
def test_valida_comune_valido(comune):
    assert valida_comune(comune) == comune.upper()


@pytest.mark.parametrize("comune", [
    "Atlantide", "Gotham", "", None
])
def test_valida_comune_non_valido(comune):
    with pytest.raises(ValueError, match="Comune/Stato non valido"):
        valida_comune(comune)
