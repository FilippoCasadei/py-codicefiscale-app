import pytest
from source.codice_fiscale import *


@pytest.mark.parametrize("cognome", ["Rossi", "D'Angelo", "O'Connor", "De Santis"])
def test_valida_cognome_positivi(cognome):
    assert valida_cognome(cognome) == cognome.upper()

@pytest.mark.parametrize("cognome", ["", "R"])
def test_valida_cognome_troppo_corto(cognome):
    with pytest.raises(ValueError):
        valida_cognome(cognome)

@pytest.mark.parametrize("cognome", ["A" * 51, "B" * 100])
def test_valida_cognome_troppo_lungo(cognome):
    with pytest.raises(ValueError):
        valida_cognome(cognome)

@pytest.mark.parametrize("cognome", ["Rossi123", "Rossi@", "Rossi-", "Rossi*", "Rossi&", "Rossi?"])
def test_valida_cognome_simboli_non_accettati(cognome):
    with pytest.raises(ValueError):
        valida_cognome(cognome)

