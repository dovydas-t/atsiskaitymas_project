


class Knyga:
    def __init__(self, autorius, pavadinimas, metai, zanras, turimas_kiekis):
        self.autorius = autorius
        self.pavadinimas = pavadinimas
        self.metai = metai
        self.zanras = zanras
        self.turimas_kiekis = turimas_kiekis
        self.pradinis_kiekis = turimas_kiekis

    def __str__(self):
        return f"{self.pavadinimas} (autorius: {self.autorius}, metai: {self.metai}) - Žanras: {self.zanras}, Turimas kiekis: {self.turimas_kiekis}"
    
    def __repr__(self):
        return (f"Knyga(autorius={repr(self.autorius)}, pavadinimas={repr(self.pavadinimas)}, "
                f"metai={self.metai}, zanras={repr(self.zanras)}, turimas_kiekis={self.turimas_kiekis})")
