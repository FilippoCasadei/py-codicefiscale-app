import string
from utils import _crea_dict_denominazione_codice_nazionale_da_csv, _formatta_stringa, _estrai_caratteri
from datetime import datetime, date


############
# COSTANTI #
############
CONVERSIONE_MESE_LETTERA = {
    '01': 'A', '02': 'B', '03': 'C', '04': 'D', '05': 'E', '06': 'H',
    '07': 'L', '08': 'M', '09': 'P', '10': 'R', '11': 'S', '12': 'T'
}
VAL_SOMMARE_GIORNO_FEMM = 40
COMUNI_COD_NAZIONALI = _crea_dict_denominazione_codice_nazionale_da_csv('source/data/tabella_comuni.csv')
STATI_COD_NAZIONALI = _crea_dict_denominazione_codice_nazionale_da_csv('source/data/tabella_comuni.csv')
COMUNI_E_STATI_COD_NAZIONALI = COMUNI_COD_NAZIONALI | STATI_COD_NAZIONALI
CONVERSIONE_CARATTERI_PARI_DISPARI = {
    "0": (0, 1), "1": (1, 0), "2": (2, 5), "3": (3, 7), "4": (4, 9), "5": (5, 13), "6": (6, 15), "7": (7, 17),
    "8": (8, 19), "9": (9, 21), "A": (0, 1), "B": (1, 0), "C": (2, 5), "D": (3, 7), "E": (4, 9), "F": (5, 13),
    "G": (6, 15), "H": (7, 17), "I": (8, 19), "J": (9, 21), "K": (10, 2), "L": (11, 4), "M": (12, 18),
    "N": (13, 20), "O": (14, 11), "P": (15, 3), "Q": (16, 6), "R": (17, 8), "S": (18, 12), "T": (19, 14),
    "U": (20, 16), "V": (21, 10), "W": (22, 22), "X": (23, 25), "Y": (24, 24), "Z": (25, 23),
}
VAL_MODULO_CARATTERE_CONTROLLO = 26
CONVERSIONE_CARATTERE_CONTROLLO = {i: lettera for i, lettera in enumerate(string.ascii_uppercase)}


#######################
# FUNZIONE PRINCIPALE #
#######################
def genera_codice_fiscale(cognome, nome, sesso, data_nascita, comune):
    """Genera il codice fiscale completo basato sui dati anagrafici.

    Args:
        cognome (str): Cognome della persona.
        nome (str): Nome della persona.
        sesso (str): Sesso ('M' o 'F').
        data_nascita (str): Data di nascita in formato GG/MM/AAAA.
        comune (str): Comune o stato di nascita.

    Returns:
        str: Codice fiscale generato.
    """
    codifica_senza_carattere_controllo = "".join([
        codifica_cognome(cognome),
        codifica_nome(nome),
        codifica_data_nascita(data_nascita, sesso),
        codifica_comune(comune)
    ])
    return "".join([codifica_senza_carattere_controllo,
                    calcola_carattere_controllo(codifica_senza_carattere_controllo)])


########################
# FUNZIONI DI CODIFICA #
########################
def codifica_cognome(cognome):
    """Codifica la parte del cognome nel codice fiscale.

    Args:
        cognome (str): Cognome della persona.

    Returns:
        str: Codifica a 3 lettere del cognome.
    """
    cognome = valida_cognome(cognome)
    return _estrai_caratteri(cognome)


def codifica_nome(nome):
    """Codifica la parte del nome nel codice fiscale.

    Args:
        nome (str): Nome della persona.

    Returns:
        str: Codifica a 3 lettere del nome.
    """
    nome = valida_nome(nome)
    return _estrai_caratteri(nome, is_nome=True)


def codifica_data_nascita(data_nascita, sesso):
    """Codifica la data di nascita e il sesso nel codice fiscale.

    Args:
        data_nascita (str): Data di nascita in formato GG/MM/AAAA.
        sesso (str): Sesso ('M' o 'F').

    Returns:
        str: Codifica a 5 caratteri della data di nascita (anno, mese, giorno).
    """
    sesso = valida_sesso(sesso)
    giorno, mese, anno = valida_data_nascita(data_nascita).split("/")
    cod_anno = anno[2:]
    cod_mese = CONVERSIONE_MESE_LETTERA[mese]
    cod_giorno = str(int(giorno) + VAL_SOMMARE_GIORNO_FEMM) if sesso == 'F' else giorno
    return "".join([cod_anno, cod_mese, cod_giorno.zfill(2)])


def codifica_comune(comune):
    """Codifica il comune o stato di nascita nel codice fiscale.

    Args:
        comune (str): Nome del comune o stato di nascita.

    Returns:
        str: Codice catastale del comune o stato di nascita.
    """
    comune = valida_comune(comune)
    return COMUNI_E_STATI_COD_NAZIONALI[comune]


def calcola_carattere_controllo(codice_senza_controllo):
    """Calcola il carattere di controllo del codice fiscale.

    Args:
        codice_senza_controllo (str): Codice fiscale senza carattere di controllo.

    Returns:
        str: Carattere di controllo calcolato.
    """
    caratteri_pari = codice_senza_controllo[1::2]
    caratteri_dispari = codice_senza_controllo[::2]
    somma = sum(CONVERSIONE_CARATTERI_PARI_DISPARI[char][0] for char in caratteri_pari)
    somma += sum(CONVERSIONE_CARATTERI_PARI_DISPARI[char][1] for char in caratteri_dispari)
    carattere_controllo = somma % VAL_MODULO_CARATTERE_CONTROLLO
    return CONVERSIONE_CARATTERE_CONTROLLO[carattere_controllo]


###########################
# FUNZIONI DI VALIDAZIONE #
###########################
def valida_cognome(cognome):
    """Valida il cognome, verificando che contenga solo lettere, accenti, apostrofi e spazi.

    Args:
        cognome (str): Cognome della persona.

    Returns:
        str: Cognome formattato e validato.

    Raises:
        ValueError: Se il cognome è troppo corto/lungo o contiene caratteri non validi.
    """
    if len(cognome) < 2 or len(cognome) > 50 or not all(char.isalpha() or char in ["'", " "] for char in cognome):
        raise ValueError("Cognome non valido. Deve contenere solo lettere, accenti, apostrofi e spazi (2-50 caratteri).")
    return _formatta_stringa(cognome)


def valida_nome(nome):
    """Valida il nome, verificando che contenga solo lettere, accenti, apostrofi e spazi.

    Args:
        nome (str): Nome della persona.

    Returns:
        str: Nome formattato e validato.

    Raises:
        ValueError: Se il nome è troppo corto/lungo o contiene caratteri non validi.
    """
    if len(nome) < 2 or len(nome) > 50 or not all(char.isalpha() or char in ["'", " "] for char in nome):
        raise ValueError("Nome non valido. Deve contenere solo lettere, accenti, apostrofi e spazi (2-50 caratteri).")
    return _formatta_stringa(nome)


def valida_sesso(sesso: str) -> str:
    """Valida il sesso, assicurandosi che sia 'M' o 'F'.

    Args:
        sesso (str): Sesso della persona ('m'/'M' o 'f'/'F').

    Returns:
        str: Sesso in maiuscolo.

    Raises:
        ValueError: Se il sesso non è 'M' o 'F'.
    """
    if sesso not in ("m", "M", "f", "F"):
        raise ValueError("Sesso non valido. Deve essere 'm'/'M' o 'f'/'F'.")
    return sesso.upper()


def valida_data_nascita(data_nascita):
    """Valida la data di nascita, verificando il formato e che sia antecedente alla data odierna.

    Args:
        data_nascita (str): Data di nascita in formato GG/MM/AAAA.

    Returns:
        str: Data di nascita validata e formattata.

    Raises:
        ValueError: Se il formato è errato o la data è futura.
    """
    try:
        data_nascita = datetime.strptime(data_nascita, "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("Data di nascita non valida. Il formato deve essere del tipo 'DD/MM/YYYY'.")

    if data_nascita > date.today():
        raise ValueError("Data di nascita non valida. Deve essere antecedente alla data odierna.")

    return data_nascita.strftime("%d/%m/%Y")


def valida_comune(comune):
    """Valida il comune o stato di nascita, assicurandosi che esista nel database.

    Args:
        comune (str): Nome del comune o stato di nascita.

    Returns:
        str: Nome del comune in maiuscolo.

    Raises:
        ValueError: Se il comune non esiste nel database.
    """
    comune = comune.upper()
    if comune not in COMUNI_E_STATI_COD_NAZIONALI:
        raise ValueError("Comune/Stato non valido. Deve essere presente un comune o uno stato estero esistente.")
    return comune
