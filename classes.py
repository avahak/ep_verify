from typing import Type, Any
from dataclasses import dataclass, fields

def cast_types(cls: Type) -> Type:
    """
    Decorator that casts the attributes of a dataclass to their annotated types 
    upon initialization if the annotated type is supported for casting here.
    """
    original_init = cls.__init__

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        original_init(self, *args, **kwargs)   
        # Perform type casting
        for field in fields(cls):
            value = getattr(self, field.name)
            if value != None:
                if field.type is str:
                    setattr(self, field.name, str(value))
                elif field.type is int:
                    setattr(self, field.name, int(value))
                elif field.type is float:
                    setattr(self, field.name, float(value))

    cls.__init__ = __init__
    return cls

@cast_types
@dataclass
class ep_rafla:
    id: int
    lyhenne: str
    nimi: str
    osoite: str
    postosoite: str
    kauposa: str
    yhdhenk: str
    yhdpuh: str

@cast_types
@dataclass
class ep_kausi:
    id: int
    vuosi: int
    kausi: str
    laji: str

@cast_types
@dataclass
class ep_lohko:
    id: int
    kausi: int
    tunnus: str
    selite: str

@cast_types
@dataclass
class ep_joukkue:
    id: int
    lyhenne: str
    nimi: str
    kausi: int
    lohko: int
    ravintola: int
    yhdhenk: str
    yhdpuh: str
    kapt: str
    kpuh: str
    varakapt: str
    vkpuh: str

@cast_types
@dataclass
class ep_jasen: 
    id: int
    jasenno: int
    etunimi: str
    suku: str
    pelaaja: str

@cast_types
@dataclass
class ep_pelaaja:
    id: int
    nimi: str
    joukkue: int
    jasen: int
    pelit: int
    v_era: int
    h_era: int
    e_erat: int
    h_peli: int
    v_peli: int
    e_peli: int
    sukupuoli: str

@cast_types
@dataclass 
class ep_ottelu:
    id: int
    lohko: int
    paiva: str
    koti: int
    vieras: int
    ktulos: int
    vtulos: int
    status: str

@cast_types
@dataclass
class ep_sarjat:
    id: int
    nimi: str
    joukkue: int
    lyhenne: str
    lohko: int
    ottelu: int
    voitto: int
    tappio: int
    v_era: int
    h_era: int
    h_peli: int
    v_peli: int

@cast_types
@dataclass
class ep_peli:
    id: int
    ottelu: int
    kp: int
    vp: int
    ktulos: int
    vtulos: int

@cast_types
@dataclass
class ep_erat:
    id: int
    peli: int
    era1: str
    era2: str
    era3: str
    era4: str
    era5: str

@cast_types
@dataclass
class ep_peli_tulokset:
    id: int
    peli: int
    ktulos: int
    vtulos: int

@cast_types
@dataclass
class ep_ottelu_tulokset:
    id: int
    ottelu: int
    ktulos: int
    vtulos: int

@cast_types
@dataclass
class ep_pelaaja_tulokset:
    id: int
    pelaaja: int
    v_era: int
    h_era: int
    v_peli: int
    h_peli: int

@cast_types
@dataclass
class ep_joukkue_tulokset:
    id: int
    joukkue: int
    v_era: int
    h_era: int
    v_peli: int
    h_peli: int
    voitto: int
    tappio: int

if __name__ == '__main__':
    e = ep_erat("55", 105, "K1", "K2", "K1", "V0", "V0")
    print(e)
    print(type(e.id))