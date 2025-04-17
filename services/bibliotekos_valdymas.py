from modules.biblioteka import Biblioteka
from modules.bibliotekininkas import Bibliotekininkas
from modules.skaitytojas import Skaitytojas
from modules.knyga import Knyga
from .file_manager import FileHandler
import random


class BibliotekosValdymas:
    def __init__(self):
        self.biblioteka = Biblioteka()
        self.bibliotekininkas = Bibliotekininkas()
        self.skaitytojas = Skaitytojas()
        self.dabartinis_skaitytojo_id = None

    def rodyti_pagrindini_meniu(self):
        print("\n=== BIBLIOTEKOS VALDYMO SISTEMA ==\n")
        print("1. Bibliotekininko prisijungimas")
        print("2. Skaitytojo prisijungimas/registracija")
        print("0. Išeiti")

    def paleidimas(self):
        while True:
            self.rodyti_pagrindini_meniu()
            pasirinkimas = input("Pasirinkite veiksmą (0-2): ")

            match pasirinkimas:
                case '1':
                    self.bibliotekininko_prisijungimas()
                case '2':
                    self.skaitytojo_prisijungimai()
                case '0':
                    print("Laukiame sugrįžtant! Programa baigta.")
                    break
                case _:
                    print("\nKlaida. Netinkamas pasirinkimas. Bandykite dar kartą.")

    def bibliotekininko_prisijungimas(self):
        print("-" * 30)
        vartotojo_vardas = input("\nVartotojo vardas: ")
        slaptazodis = input("\nSlaptažodis: ")
        if self.bibliotekininkas.autentifikuoti(vartotojo_vardas, slaptazodis):
            self.bibliotekininko_meniu()
        else:
            print("\nKlaida. Netinkami prisijungimo duomenys.")

    def skaitytojo_prisijungimai(self):
        print("\n1. Registruotas skaitytojas")
        print("2. Naujas skaitytojas")
        print("0. Atgal")
        pasirinkimas = input("Pasirinkite veiksmą (0-2): ")

        if pasirinkimas == "1":
            while True:
                try:
                    skaitytojo_id = int(input("Įveskite savo skaitytojo kortelės numerį: "))
                    break
                except ValueError:
                    print("\nKlaida. Prašome įvesti skaičius.")
            if self.skaitytojas.autentifikuoti(skaitytojo_id):
                self.dabartinis_skaitytojo_id = skaitytojo_id
                print(f"\nSkaitytojas {self.dabartinis_skaitytojo_id} prisijungė.")
                self.skaitytojo_meniu()
            else:
                print("\nToks skaitytojo kortelės numeris neegzistuoja.")
        elif pasirinkimas == "2":
            naujas_id = self.skaitytojas.sukurti_nauja_skaitytoja()
            print(f"\nJūsų naujas skaitytojo kortelės numeris yra: {naujas_id}")
            self.dabartinis_skaitytojo_id = naujas_id
            self.skaitytojo_meniu()
        elif pasirinkimas == "0":
            return
        else:
            print("\nKlaida. Netinkamas pasirinkimas.")

    def rodyti_bibliotekininko_meniu(self):
        print("\n=== BIBLIOTEKININKO MENIU ===\n")
        print("1. Pridėti naują knygą į sąrašą")
        print("2. Peržiūrėti visą knygų sąrašą")
        print("3. Pašalinti senas knygas iš sąrašo")
        print("4. Peržiūrėti pašalintų senų knygų sąrašą")
        print("5. Peržiūrėti vėluojančias knygas")
        print("6. Peržiūrėti statistiką")
        print("7. Generuoti random knygų")
        print("0. Atsijungti")

    def bibliotekininko_meniu(self):
        while True:
            self.rodyti_bibliotekininko_meniu()
            pasirinkimas = input("Pasirinkite veiksmą (0-4): ")

            match pasirinkimas:
                case '1':
                    self.biblioteka.prideti_knyga()
                case '2':
                    self.biblioteka.spausdinti_knygu_sarasa()
                case '3':
                    self.biblioteka.pasalinti_senas_knygas()
                case '4':
                    self.biblioteka.spausdinti_pasalintas_knygas()
                case '5':
                    self.skaitytojas.perziureti_veluojancias_knygas()
                case '6':
                    self.biblioteka.rodyti_detalia_statistika(self.skaitytojas.paskolintu_knygu_sarasas)
                case '7':
                    self.generuoti_knygas()
                case '0':
                    print("Atsijungta.")
                    break
                case _:
                    print("\nKlaida. Netinkamas pasirinkimas.")

    def rodyti_skaitytojo_meniu(self):
        print("\n=== SKAITYTOJO MENIU ===\n")
        print("1. Peržiūrėti visą knygų sąrašą")
        print("2. Ieškoti knygos")
        print("3. Pasiskolinti knygą")
        print("4. Peržiūrėti jūsų pasiskolintas knygas")
        print("5. Grąžinti knygą")
        print("6. Tikrinti terminus")
        print("0. Atsijungti")

    def skaitytojo_meniu(self):
        while True:
            self.rodyti_skaitytojo_meniu()
            pasirinkimas = input("Pasirinkite veiksmą (0-5): ")

            match pasirinkimas:
                case '1':
                    self.biblioteka.spausdinti_knygu_sarasa()
                case '2':
                    self.ieskoti_knygu()
                case '3':
                    self.pasiskolinti_knyga_ui()
                case '4':
                    self.perziureti_paskolintas_knygas()
                case '5':
                    self.grazinti_knyga()
                case '6':
                    self.skaitytojas.tikrinti_terminus(self.dabartinis_skaitytojo_id)
                case '0':
                    print("Atsijungta.")
                    self.dabartinis_skaitytojo_id = None
                    break
                case _:
                    print("\nKlaida. Tokio pasirinkimo nėra.")

    def ieskoti_knygu(self):
        paieskos_terminas = input("\nĮveskite paieškos terminą (pavadinimas/autorius/žanras): ").strip()
        if not paieskos_terminas:
            print("\nKlaida. Prašome įvesti paieškos terminą.")
            return

        rezultatai = self.biblioteka.ieskoti_knygu(paieskos_terminas)
        if not rezultatai:
            print(f"\nNerasta knygų, atitinkančių '{paieskos_terminas}'")
            return

        print(f"\n{len(rezultatai)} atitikmenys:")
        for i, knyga in enumerate(rezultatai, 1):
            print(f"{i}. {knyga.pavadinimas} (autorius: {knyga.autorius})")
            print(f"  Metai: {knyga.metai} | Žanras: {knyga.zanras}")
            print(f"  Turimas kiekis: {knyga.turimas_kiekis}")
            print("-" * 40)

    def pasiskolinti_knyga_ui(self):
        if not self.dabartinis_skaitytojo_id:
            print("\nNeprisijungęs skaitytojas.")
            return
        
        available_books = [book for book in self.biblioteka.knygu_sarasas if book.turimas_kiekis > 0]   
        if not available_books:
            print("\nŠiuo metu visos knygos yra pasiskolintos.")
            return
            
        print("\n=== PRIEINAMOS KNYGOS ===")
        for i, knyga in enumerate(available_books, 1):
            print(f"{i}. {knyga}")
        
        try:
            pasirinkimas = int(input("\nĮveskite knygos numerį, kurią norite pasiskolinti (0 - atgal): "))
            if pasirinkimas == 0:
                return
            if 1 <= pasirinkimas <= len(available_books):
                pasirinkta_knyga = available_books[pasirinkimas - 1]
                if self.skaitytojas.pasiskolinti_knyga_logic(self.dabartinis_skaitytojo_id, pasirinkta_knyga):
                    pasirinkta_knyga.turimas_kiekis -= 1
                    FileHandler.write_to_pickle(self.biblioteka.failas, self.biblioteka.knygu_sarasas)
                else:
                    print("\nPaskolinti knygos nepavyko.")
            else:
                print("\nKlaida. Netinkamas pasirinkimas.")
        except ValueError:
            print("\nKlaida. Įrašykite skaičių.")

    def perziureti_paskolintas_knygas(self):
        if not self.dabartinis_skaitytojo_id:
            print("\nNeprisijungęs skaitytojas.")
            return

        pasiskolintos_knygos = self.skaitytojas.paskolintu_knygu_sarasas.get(self.dabartinis_skaitytojo_id, [])
        if pasiskolintos_knygos:
            print("\nJŪSŲ PASISKOLINTOS KNYGOS:")
            for i, knyga in enumerate(pasiskolintos_knygos, 1):
                print(f"{i}. {knyga['knyga'].pavadinimas} (autorius: {knyga['knyga'].autorius}, metai: {knyga['knyga'].metai}) - Grąžinimo data: {knyga['grąžinimo_data']}")
        else:
            print("\nNeturite pasiskolintų knygų.")

    def grazinti_knyga(self):
        if not self.dabartinis_skaitytojo_id:
            print("\nNeprisijungęs skaitytojas.")
            return

        skaitytojo_id = self.dabartinis_skaitytojo_id
        pasiskolintos = self.skaitytojas.paskolintu_knygu_sarasas.get(skaitytojo_id, [])

        if not pasiskolintos:
            print("\nNeturite pasiskolintų knygų.")
            return

        print("\nPasiskolintos knygos:")
        for i, knyga in enumerate(pasiskolintos, 1):
            print(f"{i}. {knyga['knyga'].pavadinimas} - {knyga['knyga'].autorius}")

        try:
            pasirinkimas = int(input("Įveskite grąžinamos knygos numerį: "))
            if 1 <= pasirinkimas <= len(pasiskolintos):
                grazinta_knyga = pasiskolintos.pop(pasirinkimas - 1)
                for knyga in self.biblioteka.knygu_sarasas:
                    if knyga.pavadinimas == grazinta_knyga['knyga'].pavadinimas:
                        knyga.turimas_kiekis += 1
                        break
                print(f"\nKnyga „{grazinta_knyga['knyga'].pavadinimas}“ grąžinta sėkmingai.")
            else:
                print("\nKlaida. Neteisingas pasirinkimas.")
        except ValueError:
            print("\nKlaida. Įveskite teisingą skaičių.")

        self.skaitytojas.paskolintu_knygu_sarasas[skaitytojo_id] = pasiskolintos

        FileHandler.write_to_pickle(self.skaitytojas.paskolintu_knygu_failas, self.skaitytojas.paskolintu_knygu_sarasas)
        FileHandler.write_to_pickle(self.biblioteka.failas, self.biblioteka.knygu_sarasas)

    def generuoti_knygas(self):
        try:
            gen_knygu_skaicius = int(input("Įveskite generuojamų knygų skaičių: "))
            gen_knygu_max_kiekis = int(input("Įveskite maksimalų kiekį kiekvienai knygai: "))

            knygu_failas = "C:\\Users\\djfkj\\Desktop\\python_pagrindai\\atsiskaitymas123\\atsiskaitymas_project\\sarasai\\knygu_sarasas.pkl"
            autoriai = ["Jonas Jonaitis", "Petras Petraitis", "Ona Onaitė", "Kazys Kazlauskas", "Agnė Agnėlytė"]
            pavadinimai = ["Paslaptingas miškas", "Kelionė į Marsą", "Meilės istorija", "Istorijos vadovėlis", "Programavimo pagrindai"]
            zanrai = ["Fantastika", "Romantika", "Istorija", "Mokslas", "Nuotykiai"]

            # Debugging: Print initial data
            print(f"Generating {gen_knygu_skaicius} books with max quantity {gen_knygu_max_kiekis}")
            print(f"Authors: {autoriai}")
            print(f"Titles: {pavadinimai}")
            print(f"Genres: {zanrai}")

            knygu_sarasas = FileHandler.read_from_pickle(knygu_failas, [])

            for _ in range(gen_knygu_skaicius):
                autorius = random.choice(autoriai)
                pavadinimas = random.choice(pavadinimai)
                zanras = random.choice(zanrai)
                metai = random.randint(1900, 2025)
                turimas_kiekis = random.randint(1, gen_knygu_max_kiekis)

                nauja_knyga = Knyga(autorius, pavadinimas, metai, zanras, turimas_kiekis)
                knygu_sarasas.append(nauja_knyga)

            # Debugging: Print generated books
            print(f"Generated books: {knygu_sarasas}")

            FileHandler.write_to_pickle(knygu_failas, knygu_sarasas)

            print("\nKnygų sąrašas sėkmingai papildytas atsitiktinėmis knygomis!")
        except ValueError:
            print("\nKlaida. Prašome įvesti skaičius.")
        except Exception as e:
            print(f"\nĮvyko klaida: {e}")

