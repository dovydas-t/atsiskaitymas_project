


class Bibliotekininkas:
    def __init__(self, vartotojo_vardas="admin", slaptazodis="admin123"):
        self.vartotojo_vardas = vartotojo_vardas
        self.slaptazodis = slaptazodis

    def autentifikuoti(self, vartotojo_vardas, slaptazodis):
        return vartotojo_vardas == self.vartotojo_vardas and slaptazodis == self.slaptazodis
   