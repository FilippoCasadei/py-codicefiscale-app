import string
import unicodedata
from datetime import datetime, date
from comuni import crea_dict_denominazione_codice_nazionale_da_csv


# Costanti
VOCALI = {'A', 'E', 'I', 'O', 'U'}
CONSONANTI = {'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z'}
CONVERSIONE_MESE_LETTERA = {
    '01': 'A', '02': 'B', '03': 'C', '04': 'D', '05': 'E', '06': 'H',
    '07': 'L', '08': 'M', '09': 'P', '10': 'R', '11': 'S', '12': 'T'
}
VAL_SOMMARE_GIORNO_FEMM = 40
COMUNI = crea_dict_denominazione_codice_nazionale_da_csv('source/data/tabella_comuni.csv')
STATI = crea_dict_denominazione_codice_nazionale_da_csv('source/data/tabella_comuni.csv')
COMUNI_E_STATI = COMUNI | STATI   # Unione dei due dizionari (python 3.9+)
CONVERSIONE_CARATTERI_PARI_DISPARI = {
    "0": (0, 1), "1": (1, 0), "2": (2, 5), "3": (3, 7), "4": (4, 9), "5": (5, 13), "6": (6, 15), "7": (7, 17),
    "8": (8, 19), "9": (9, 21), "A": (0, 1), "B": (1, 0), "C": (2, 5), "D": (3, 7), "E": (4, 9), "F": (5, 13),
    "G": (6, 15), "H": (7, 17), "I": (8, 19), "J": (9, 21), "K": (10, 2), "L": (11, 4), "M": (12, 18),
    "N": (13, 20), "O": (14, 11), "P": (15, 3), "Q": (16, 6), "R": (17, 8), "S": (18, 12), "T": (19, 14),
    "U": (20, 16), "V": (21, 10), "W": (22, 22), "X": (23, 25), "Y": (24, 24), "Z": (25, 23),
}
VAL_MODULO_NUMERO_CONTROLLO = 26
CONVERSIONE_CARATTERE_CONTROLLO = {i: lettera for i, lettera in enumerate(string.ascii_uppercase)}

class CodiceFiscale:
    """
    Classe per la generazione del Codice Fiscale basata sui dati anagrafici di una persona.
    """

    def __init__(self, cognome: str, nome: str, sesso: str, data_nascita: str, comune: str) -> None:
        """
        Inizializza la classe con i dati anagrafici della persona.

        :param cognome: Cognome della persona
        :type nome: str
        :param nome: Nome della persona
        :type cognome: str
        :param sesso: Sesso della persona ('M' o 'F')
        :type sesso: str
        :param data_nascita: Data di nascita (GG/MM/YYYY)
        :type data_nascita: str
        :param comune: Comune o Stato di nascita
        :type comune: str
        """
        self.cognome = self._valida_cognome(cognome)
        self.nome = self._valida_nome(nome)
        self.sesso = self._valida_sesso(sesso)
        self.data_nascita = self._valida_data_nascita(data_nascita)
        self.comune = self._valida_comune(comune)

    def genera_codice_fiscale(self) -> str:
        """
        Genera il codice fiscale completo della persona.

        :returns: Codice fiscale generato
        :rtype: str
        """
        codifica_senza_carattere_controllo = "".join([
            self.codifica_cognome(),
            self.codifica_nome(),
            self.codifica_data_nascita(),
            self.codifica_comune()
        ])
        return "".join([codifica_senza_carattere_controllo,
                        self.calcola_carattere_controllo(codifica_senza_carattere_controllo)])

    def codifica_cognome(self) -> str:
        """
        Codifica la prima tripletta di lettere per il cognome.

        :returns: Codifica a 3 lettere del cognome
        :rtype: str
        """
        return self._estrai_caratteri(self.cognome)

    def codifica_nome(self) -> str:
        """
        Codifica la seconda tripletta di lettere per il nome.

        :returns: Codifica a 3 lettere del nome
        :rtype: str
        """
        return self._estrai_caratteri(self.nome, is_nome=True)

    def codifica_data_nascita(self) -> str:
        """
        Codifica in ordine:
            - cod_anno: 2 numeri raffiguranti decina e unità
            - cod_mese: 1 lettera ottenuta convertendo il valore numerico del mese secondo la tabella di conversione
            - cod_giorno: 2 numeri raffiguranti il giorno stesso se maschio, altrimenti il giorno sommato a 40

        :returns: Codifica a 5 caratteri della data di nascita (cod_anno+cod_mese+cod_giorno)
        :rtype: str
        """
        giorno, mese, anno = self.data_nascita.split("/")
        cod_anno = anno[2:]
        cod_mese = CONVERSIONE_MESE_LETTERA[mese]
        cod_giorno = str(int(giorno) + VAL_SOMMARE_GIORNO_FEMM) if self.sesso == 'F' else giorno
        return "".join([cod_anno, cod_mese, cod_giorno])

    def codifica_comune(self) -> str:
        """
        Codifica il comune o lo stato di nascita utilizzando il codice nazionale.

        :returns: Codice nazionale del comune o dello stato di nascita
        :rtype: str
        """
        return COMUNI_E_STATI[self.comune]

    @staticmethod
    def calcola_carattere_controllo(codice_senza_controllo: str) -> str:
        """
        Calcola il carattere di controllo del codice fiscale.

        :param codice_senza_controllo: Codice fiscale senza carattere di controllo
        :type codice_senza_controllo: str
        :returns: Carattere di controllo calcolato
        :rtype: str
        """
        caratteri_pari = codice_senza_controllo[1::2]
        caratteri_dispari = codice_senza_controllo[::2]
        somma = sum(CONVERSIONE_CARATTERI_PARI_DISPARI[char][0] for char in caratteri_pari)
        somma += sum(CONVERSIONE_CARATTERI_PARI_DISPARI[char][1] for char in caratteri_dispari)
        numero_controllo = somma % VAL_MODULO_NUMERO_CONTROLLO
        return CONVERSIONE_CARATTERE_CONTROLLO[numero_controllo]

    def _valida_cognome(self, cognome: str) -> str:
        """
        Verifica che il cognome sia una stringa di lunghezza compresa tra 2 e 50 e che non ci siano caratteri
        all'infuori di lettere, accenti, apostrofi e spazi.

        :param cognome: Cognome
        :type cognome: str
        :returns: Cognome validato e formattato
        :rtype: str
        :raises ValueError: Se la lunghezza o i caratteri al suo interno non sono validi.
        """
        if len(cognome) < 2 or len(cognome) > 50:
            raise ValueError("Cognome non valido. Il numero di caratteri deve essere compreso tra 2 e 50")
        for char in cognome:
            if not (char.isalpha() or char in ["'", " "]):
                raise ValueError("Cognome non valido. I caratteri accettati sono  lettere, accenti, apostrofi e spazi")
        cognome_validato = self._formatta_stringa(cognome)
        return cognome_validato

    def _valida_nome(self, nome: str) -> str:
        """
        Verifica che il nome sia una stringa di lunghezza compresa tra 2 e 50 e che non ci siano caratteri
        all'infuori di lettere, accenti, apostrofi e spazi.

        :param nome: Nome
        :type nome: str
        :returns: Nome validato e formattato
        :rtype: str
        :raises ValueError: Se la lunghezza o i caratteri al suo interno non sono validi.
        """
        if len(nome) < 2 or len(nome) > 50:
            raise ValueError("Cognome non valido. Il numero di caratteri deve essere compreso tra 2 e 50")
        for char in nome:
            if not (char.isalpha() or char in ["'", " "]):
                raise ValueError("Cognome non valido. I caratteri accettati sono  lettere, accenti, apostrofi e spazi")
        nome_validato = self._formatta_stringa(nome)
        return nome_validato

    def _valida_data_nascita(self, data_nascita: str) -> str:
        """
        Verifica che la data di nascita sia nel formato corretto e che non sia futura alla data corrente.

        :param data_nascita: Data di nascita
        :type data_nascita: str
        :returns: Data di nascita validata
        :rtype: str
        :raises ValueError: Se il formato non è valido o se la data è futura a quella corrente.
        """
        giorno, mese, anno = data_nascita.split("/")
        # Controllo formato
        self._valida_giorno(giorno)
        self._valida_mese(mese)
        self._valida_anno(anno)
        # Controllo temporale (1900 <= data <= oggi)
        data_corrente = date.today()
        data_nascita_formattata = datetime.strptime(data_nascita, "%d/%m/%Y").date()
        if data_nascita_formattata <= data_corrente:
            return data_nascita
        else:
            raise ValueError("Data di nascita non valida. La data non può essere riferito a un giorno futuro.")

    @staticmethod
    def _valida_anno(anno: str) -> str:
        """
        Verifica che l'anno sia una stringa numerica di 4 cifre.

        :param anno: Anno di nascita
        :type anno: str
        :returns: Anno validato
        :rtype: str
        :raises ValueError: Se l'anno non è valido.
        """
        if len(anno) != 4 or not anno.isdigit():
            raise ValueError("Anno non valido. Deve essere un valore numerico a 4 cifre.")
        return anno

    @staticmethod
    def _valida_mese(mese: str) -> str:
        """
        Verifica che il mese sia nel formato numerico corretto.

        :param mese: Mese di nascita
        :type mese: str
        :returns: Mese validato
        :rtype: str
        :raises ValueError: Se il mese non è valido.
        """
        if mese not in CONVERSIONE_MESE_LETTERA:
            raise ValueError("Mese non valido. Deve essere un valore numerico tra '01' e '12'.")
        return mese

    @staticmethod
    def _valida_giorno(giorno: str) -> str:
        """
        Verifica che il giorno sia nel formato corretto (1-31).

        :param giorno: Giorno di nascita
        :type giorno: str
        :returns: Giorno validato
        :rtype: str
        :raises ValueError: Se il giorno non è valido.
        """
        if not giorno.isdigit() or not (1 <= int(giorno) <= 31):
            raise ValueError("Giorno non valido. Deve essere un valore numerico tra 1 e 31.")
        return giorno.zfill(2)

    @staticmethod
    def _valida_sesso(sesso: str) -> str:
        """
        Verifica che il sesso sia 'M' o 'F'.

        :param sesso: Sesso della persona
        :type sesso: str
        :returns: Sesso validato
        :rtype: str
        :raises ValueError: Se il sesso non è valido.
        """
        if sesso not in ("m", "M", "f", "F"):
            raise ValueError("Sesso non valido. Deve essere 'M' o 'F'.")
        return sesso

    @staticmethod
    def _valida_comune(comune: str) -> str:
        """
        Verifica che il comune o stato sia presente nel dizionario dei comuni e stati esistenti.

        :param comune: Comune di nascita
        :type comune: str
        :returns: Comune validato in maiuscolo
        :rtype: str
        :raises ValueError: Se il comune non è valido.
        """
        if comune.upper() in COMUNI_E_STATI:
            return comune.upper()
        raise ValueError("Comune/Stato non valido. Deve essere presente nella tabella dei comuni o degli stati.")


    @staticmethod
    def _rimuovi_accenti(stringa: str) -> str:
        stringa_normalizzata = unicodedata.normalize('NFD', stringa)
        return ''.join(c for c in stringa_normalizzata if unicodedata.category(c) != 'Mn')

    @staticmethod
    def _formatta_stringa(stringa: str) -> str:
        return CodiceFiscale._rimuovi_accenti(stringa.replace(' ', '')).upper()

    @staticmethod
    def _get_consonanti(stringa: str) -> str:
        return ''.join(char for char in stringa if char in CONSONANTI)

    @staticmethod
    def _get_vocali(stringa: str) -> str:
        return ''.join(char for char in stringa if char in VOCALI)

    @staticmethod
    def _estrai_caratteri(stringa: str, is_nome: bool = False) -> str:
        consonanti = CodiceFiscale._get_consonanti(stringa)
        vocali = CodiceFiscale._get_vocali(stringa)
        if is_nome and len(consonanti) >= 4:
            return consonanti[0] + consonanti[2] + consonanti[3]
        codifica = consonanti[:3] if len(consonanti) >= 3 else consonanti + vocali[:3 - len(consonanti)]
        return codifica.ljust(3, 'X')