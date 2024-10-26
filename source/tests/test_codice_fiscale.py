import pytest
from codice_fiscale import CodiceFiscale


# Fixture per le persone

@pytest.fixture
def persona_valida():
    """Fixture per una persona con nome e cognome validi."""
    return CodiceFiscale(cognome="Rossi", nome="Mario", anno="1980", mese="03", giorno="25", sesso="M", comune="Roma")

@pytest.fixture
def persona_nome_consonanti():
    """Fixture per una persona con un nome con molte consonanti."""
    return Persona(cognome="Colombo", nome="Cristoforo", anno="1451", mese="10", giorno="31", sesso="M", comune="Genova")

@pytest.fixture
def persona_nome_vocali():
    """Fixture per una persona con un nome contenente solo vocali."""
    return Persona(cognome="Ove", nome="Aia", anno="1995", mese="05", giorno="12", sesso="F", comune="Napoli")

@pytest.fixture
def persona_nome_corto():
    """Fixture per una persona con nome molto corto."""
    return Persona(cognome="Wu", nome="Li", anno="1990", mese="07", giorno="09", sesso="M", comune="Milano")

@pytest.fixture
def persona_nome_spazi():
    """Fixture per una persona con nome o cognome con spazi extra."""
    return Persona(cognome=" Rossi  ", nome=" Maria ", anno="1985", mese="08", giorno="15", sesso="F", comune="Torino")

@pytest.fixture
def persona_vuota():
    """Fixture per una persona con nome e cognome vuoti."""
    return Persona(cognome="", nome="", anno="2000", mese="01", giorno="01", sesso="M", comune="Roma")

def test_codifica_fiscale(persona_valida):
    """Test per la corretta codifica del cognome."""
    assert persona_valida.genera_codice_fiscale() == "RSSMRA80C25H501N"

# Test codifica del cognome

def test_codifica_cognome_valida(persona_valida):
    """Test per la corretta codifica del cognome."""
    cf = CodiceFiscale(persona_valida)
    assert cf.codifica_cognome() == "RSS"

def test_codifica_cognome_nome_corto(persona_nome_corto):
    """Test per codifica del cognome con nome e cognome corti."""
    cf = CodiceFiscale(persona_nome_corto)
    assert cf.codifica_cognome() == "WUX"

def test_codifica_cognome_con_spazi(persona_nome_spazi):
    """Test per codifica del cognome con spazi extra."""
    cf = CodiceFiscale(persona_nome_spazi)
    assert cf.codifica_cognome() == "RSS"

def test_codifica_cognome_nome_vuoto(persona_vuota):
    """Test per cognome vuoto."""
    cf = CodiceFiscale(persona_vuota)
    with pytest.raises(ValueError):
        cf.codifica_cognome()


# Test codifica del nome

def test_codifica_nome_valida(persona_valida):
    """Test per la corretta codifica del nome."""
    cf = CodiceFiscale(persona_valida)
    assert cf.codifica_nome() == "MRA"

def test_codifica_nome_con_consonanti(persona_nome_consonanti):
    """Test per un nome con molte consonanti (Cristoforo)."""
    cf = CodiceFiscale(persona_nome_consonanti)
    assert cf.codifica_nome() == "CST"

def test_codifica_nome_con_vocali(persona_nome_vocali):
    """Test per un nome contenente solo vocali."""
    cf = CodiceFiscale(persona_nome_vocali)
    assert cf.codifica_nome() == "AIA"

def test_codifica_nome_vuoto(persona_vuota):
    """Test per nome vuoto."""
    cf = CodiceFiscale(persona_vuota)
    with pytest.raises(ValueError):
        cf.codifica_nome()


# Test codifica dell'anno

def test_codifica_anno(persona_valida):
    cf = CodiceFiscale(persona_valida)
    assert cf.codifica_anno() == "80"


# Test codifica del mese
# Test codifica del giorno
# Test codifica del comune

def test_codifica_comune(persona_valida):
    """Test per la corretta codifica del comune."""
    cf = CodiceFiscale(persona_valida)
    assert cf.codifica_comune() == "H501"


# Test carattere di controllo
def test_carattere_controllo(persona_valida):
    """Test per il corretto calcolo del carattere di controllo."""
    cf = CodiceFiscale(persona_valida)
    assert cf.carattere_controllo() == "N"

# Test funzioni interne

def test_rimuovi_accenti():
    """Test per la rimozione degli accenti."""
    assert CodiceFiscale._rimuovi_accenti("Caffè") == "Caffe"
    assert CodiceFiscale._rimuovi_accenti("Èlia") == "Elia"

def test_formatta_stringa():
    """Test per la formattazione delle stringhe (spazi e accenti)."""
    assert CodiceFiscale._formatta_stringa(" Rossi ") == "ROSSI"
    assert CodiceFiscale._formatta_stringa("Caffè") == "CAFFE"


def test_get_consonanti():
    """Test per l'estrazione di consonanti da una stringa."""
    assert CodiceFiscale._get_consonanti("CRISTOFORO") == "CRST"   # Prende al massimo 4 consonanti
    assert CodiceFiscale._get_consonanti("AIA") == ""  # Nessuna consonante


def test_get_vocali():
    """Test per l'estrazione di vocali da una stringa."""
    assert CodiceFiscale._get_vocali("CRISTOFORO") == "IOOO"
    assert CodiceFiscale._get_vocali("BC") == ""  # Nessuna vocale


def test_estrai_caratteri_nome():
    """Test per l'estrazione dei caratteri per un nome."""
    assert CodiceFiscale._estrai_caratteri("CRISTOFORO", is_nome=True) == "CST"
    assert CodiceFiscale._estrai_caratteri("CRIS", is_nome=True) == "CRS"
    assert CodiceFiscale._estrai_caratteri("AIA", is_nome=True) == "AIA"


def test_estrai_caratteri_cognome():
    """Test per l'estrazione dei caratteri per un cognome."""
    assert CodiceFiscale._estrai_caratteri("ROSSI") == "RSS"
    assert CodiceFiscale._estrai_caratteri("OVE") == "VOE"


def test_aggiungi_simbolo():
    """Test per l'aggiunta del simbolo 'X' se i caratteri estratti sono meno di 3."""
    assert CodiceFiscale._aggiungi_simbolo("RS") == "RSX"
    assert CodiceFiscale._aggiungi_simbolo("A") == "AXX"
    assert CodiceFiscale._aggiungi_simbolo("RSS") == "RSS"  # Nessuna X se sono già 3 caratteri
