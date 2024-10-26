import pytest
from source.codice_fiscale import CodiceFiscale


@pytest.fixture
def persona_valida():
    """Fixture per una persona con nome e cognome validi."""
    return CodiceFiscale(cognome="Rossi", nome="Mario", data_nascita="28/01/2004", sesso="M", comune="RomA")

def test_codifica_cognome_valida(persona_valida):
    assert persona_valida.genera_codice_fiscale() == "RSSMRA04A28H501B"
