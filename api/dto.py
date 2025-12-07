from typing import Optional, Literal

from pydantic import Field, BaseModel


class OsobaPoszkodowana(BaseModel):
    imie: Optional[str] = Field(None)
    nazwisko: Optional[str] = Field(None)
    pesel: Optional[str] = Field(None)
    adres_zamieszkania: Optional[str] = Field(None)
    data_urodzenia: Optional[str] = Field(None)
    plec: Optional[str] = Field(None)
    seria_dokumentu: Optional[str] = Field(
        None, description="Rodzaj, seria i numer dokumentu potwierdzającego tożsamość"
    )


class OkolicznoscWypadku(BaseModel):
    data_wypadku: Optional[str] = Field(None)
    godzina_wypadku: Optional[str] = Field(None)
    miejsce_wypadku: Optional[str] = Field(None)
    rodzaj_czynnosci: Optional[str] = Field(None)
    opis_okolicznosci: Optional[str] = Field(None)
    przyczyny: Optional[str] = Field(None)
    opis_mechanizmu: Optional[str] = Field(None)


class SkutkiWypadku(BaseModel):
    obrazenia: Optional[str] = Field(None)
    hospitalizacja: Optional[str] = Field(None)
    czas_niezdolnosci: Optional[str] = Field(None)
    leczenie: Optional[str] = Field(None)


class ProcesDecyzyjny(BaseModel):
    czy_uznano_za_wypadek: Optional[bool] = Field(None)
    uzasadnienie: Optional[str] = Field(None)
    wymagane_uzupelnienia: Optional[list[str]] = Field(None)


class InformacjaOWypadku(BaseModel):
    pierwsza_pomoc: bool = Field(None, description="Czy była udzielona pomoc medyczna")
    placowka: str | None = Field(
        None,
        description="Nazwa placówki, w której została udzielona "
                    "pierwsza pomoc (jeżeli zostałą udzielona)",
    )
    urazy: str = Field(description="Rodzaj doznanych urazów")
    opis: str = Field(
        description="Szczegółowy opis okoliczności, miejsca i przyczyn wypadku"
    )


class ZawiadomienieOWypadku(BaseModel):
    poszkodowany: Optional[OsobaPoszkodowana] = None
    informacje_o_wypadku: InformacjaOWypadku


class DescriptionVerificationResult(BaseModel):
    szansa_uwzglednienia_ze_byl_nagly: float = Field(
        description=(
            "Ocena probabilistyczna (0.0–1.0), na ile opis jednoznacznie wskazuje, "
            "że zdarzenie było nagłe. "
            "0.0 = brak informacji, 0.1–0.3 = słabe przesłanki, "
            "0.31–0.6 = częściowe przesłanki, 0.61–0.9 = mocne, "
            "1.0 = jednoznaczne potwierdzenie."
        )
    )

    szansa_ze_stal_sie_podczas_pracy: float = Field(
        description=(
            "Ocena probabilistyczna (0.0–1.0), na ile opis wskazuje, "
            "że zdarzenie nastąpiło podczas wykonywania pracy lub w związku z pracą. "
            "Wartości pośrednie są dopuszczalne przy niepełnych przesłankach."
        )
    )

    szansa_przyczyny_zewnetrznej: float = Field(
        description=(
            "Ocena probabilistyczna (0.0–1.0), na ile opis sugeruje istnienie "
            "przyczyny zewnętrznej zdarzenia. "
            "Nie wolno zgadywać — tylko to, co wynika z tekstu."
        )
    )

    szansa_urazu_lub_smierci: float = Field(
        description=(
            "Ocena probabilistyczna (0.0–1.0), na ile opis potwierdza wystąpienie "
            "urazu lub śmierci. "
            "Lekkie obrażenia lub samo 'uderzenie' to nie gwarancja urazu."
        )
    )

    reasoning: str = Field(
        default="",
        description=(
            "Opcjonalne krótkie uzasadnienie oceny. Model może wypisać, "
            "dlaczego każda przesłanka otrzymała konkretną wartość probabilistyczną. "
            "Pomaga w stabilizacji wyników i weryfikacji oceny."
        ),
    )

    proponowana_tresc_uzasadnienia: str = Field(
        description=(
            "Gotowy, sformalizowany tekst uzasadnienia do Karty Wypadku. "
            "Musi być napisany językiem urzędowym, w formacie: "
            "'W dniu [DATA] podczas wykonywania [CZYNNOŚĆ] doszło do [ZDARZENIE]. "
            "W wyniku zdarzenia poszkodowany doznał [URAZ]. "
            "Zdarzenie spełnia/nie spełnia przesłanek definicji wypadku przy pracy, ponieważ...'"
        )
    ),

    status: Literal["Do akceptacji", "Do weryfikacji ręcznej", "Do odrzucenia"] = (
        Field(description="Status wniosku. Sam decydujesz, "
                          "czy jest do zaakceptowania, do odrzucenia, czy do weryfikacji przez człowieka"))


class WyjasnieniaPoszkodowanego(BaseModel):
    okolicznosci_i_przyczyny: str = Field(
        ...,
        description=(
            "Szczegółowy opis okoliczności i przyczyn wypadku według poszkodowanego. "
            "Powinien zawierać chronologię zdarzenia, działania wykonywane w momencie wypadku "
            "oraz czynniki zewnętrzne, które mogły wpłynąć na zdarzenie."
        )
    )
    czy_udzielono_pierwszej_pomocy: Optional[bool] = Field(
        None,
        description="Informacja, czy w momencie wypadku została udzielona pierwsza pomoc medyczna"
    )
    nazwa_placowki_sluzby_zdrowia: Optional[str] = Field(
        None,
        description="Nazwa placówki medycznej, w której poszkodowany otrzymał pierwszą pomoc (jeżeli dotyczy)"
    )


class Decision(BaseModel):
    status: str
    uzasadnienie: Optional[str] = Field(description="Opis okoliczności i przyczyn wypadku")
    braki: Optional[list[str]] = None
    wiadomosc_do_klienta: Optional[str] = None


class FormDataInput(BaseModel):
    notification_desc: str = ""  # Opis ze zgłoszenia
    victim_desc: str = ""  # Opis z wyjaśnień (lub czatu)
    injuries: str = ""
    activities: str = ""
    external_cause: str = ""


class ValidationResult(BaseModel):
    feedback: str = Field(
        description=(
            "Krótka, ekspercka informacja zwrotna dla użytkownika (max 3-4 zdania). "
            "Ocenia 4 filary wypadku: Nagłość, Przyczyna Zewnętrzna, Uraz, Związek z pracą. "
            "Jeśli brakuje przyczyny zewnętrznej, zawiera pytanie pomocnicze."
        )
    )
    is_complete: bool = Field(
        description="Czy opis zawiera wszystkie 4 elementy wymagane ustawowo (True/False)."
    )
