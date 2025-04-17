from services.file_manager import FileHandler
from datetime import datetime
from tabulate import tabulate
from .knyga import Knyga


class Biblioteka:
    def __init__(self):
        self.failas = "C:\\Users\\djfkj\\Desktop\\python_pagrindai\\atsiskaitymas123\\atsiskaitymas_project\\sarasai\\knygu_sarasas.pkl"
        self.pasalintu_knygu_failas = "C:\\Users\\djfkj\\Desktop\\python_pagrindai\\atsiskaitymas123\\atsiskaitymas_project\\sarasai\\pasalintos_knygos.pkl"
        self.knygu_sarasas = FileHandler.read_from_pickle(self.failas, [])

    def prideti_knyga(self, knyga):
        self.knygu_sarasas.append(knyga)
        return FileHandler.write_to_pickle(self.failas, self.knygu_sarasas)
    
    def spausdinti_knygu_sarasa(self):
        if not self.knygu_sarasas:
            print("\nBibliotekoje nėra knygų.")
            return

        print("\n=== KNYGOS BIBLIOTEKOJE ===")
        table = [[i + 1, knyga.pavadinimas, knyga.autorius, knyga.metai, knyga.zanras, knyga.turimas_kiekis]
                for i, knyga in enumerate(self.knygu_sarasas)]
        headers = ["#", "Pavadinimas", "Autorius", "Metai", "Žanras", "Kiekis"]
        print(tabulate(table, headers=headers, tablefmt="grid"))

    def ieskoti_knygu(self, paieskos_terminas):
        rezultatai = []
        paieskos_terminas = paieskos_terminas.lower()
        for knyga in self.knygu_sarasas:
            if (paieskos_terminas in knyga.pavadinimas.lower() or
                    paieskos_terminas in knyga.autorius.lower() or
                    paieskos_terminas in knyga.zanras.lower()):
                rezultatai.append(knyga)
        return rezultatai

    def pasalinti_senas_knygas(self):
        if not self.knygu_sarasas:
            print("\nNėra knygų, kurias būtų galima pašalinti.")
            return

        while True:
            try:
                metai = int(input("Įveskite metus (senesnės nei šie metai knygos bus pašalintos): "))
                break
            except ValueError:
                print("\nKlaida. Prašome įvesti skaičių.")

        pasalintos_knygos = [knyga for knyga in self.knygu_sarasas if knyga.metai < metai]
        self.knygu_sarasas = [knyga for knyga in self.knygu_sarasas if knyga.metai >= metai]

        if not pasalintos_knygos:
            print(f"\nNerasta knygų, senesnių nei {metai}.")
            return

        book_quantities = {}
        for knyga in pasalintos_knygos:
            if knyga.pavadinimas in book_quantities:
                book_quantities[knyga.pavadinimas] += knyga.turimas_kiekis
            else:
                book_quantities[knyga.pavadinimas] = knyga.turimas_kiekis

        FileHandler.write_to_pickle(self.failas, self.knygu_sarasas)

        esamos_pasalintos = FileHandler.read_from_pickle(self.pasalintu_knygu_failas, [])
        FileHandler.write_to_pickle(self.pasalintu_knygu_failas, esamos_pasalintos + pasalintos_knygos)

        print(f"\nPašalintos {len(pasalintos_knygos)} knygos:")
        for knyga in pasalintos_knygos:
            print(f"- {knyga.pavadinimas} ({knyga.metai}) - Kiekis: {knyga.turimas_kiekis}")

        print("\nBendra pašalintų knygų statistika:")
        for pavadinimas, kiekis in book_quantities.items():
            print(f"- {pavadinimas}: {kiekis} vnt.")

    def spausdinti_pasalintas_knygas(self):
        pasalintos_knygos = FileHandler.read_from_pickle(self.pasalintu_knygu_failas, [])
        if not pasalintos_knygos:
            print("-" * 30)
            print("\nArchyve nėra pašalintų knygų.")
            return

        print("\n=== PAŠALINTŲ KNYGŲ ARCHYVAS")
        table = [[i + 1, knyga.pavadinimas, knyga.autorius, knyga.metai, knyga.turimas_kiekis]
                for i, knyga in enumerate(pasalintos_knygos)]
        headers = ["#", "Pavadinimas", "Autorius", "Metai", "Kiekis"]
        print(tabulate(table, headers=headers, tablefmt="grid"))

    def prideti_knyga(self):
        print("\n=== PRIDĖTI NAUJĄ KNYGĄ ===")
        autorius = input("Autorius: ")
        pavadinimas = input("Pavadinimas: ")
        zanras = input("Žanras: ")
        
        while True:
            try:
                metai = int(input("Metai: "))
                dabartiniai_metai = datetime.now().year
                if metai > dabartiniai_metai:
                    print(f"\nKlaida. Metai negali būti ateityje ({dabartiniai_metai}).")
                    continue
                break
            except ValueError:
                print("\nKlaida. Prašome įvesti skaičius.")
        
        while True:
            try:
                turimas_kiekis = int(input("Kiekis: "))
                if turimas_kiekis <= 0:
                    print("\nKlaida. Kiekis turi būti teigiamas skaičius.")
                    continue
                break
            except ValueError:
                print("\nKlaida. Prašome įvesti skaičius.")

        nauja_knyga = Knyga(autorius, pavadinimas, metai, zanras, turimas_kiekis)
        self.knygu_sarasas.append(nauja_knyga)
        if FileHandler.write_to_pickle(self.failas, self.knygu_sarasas):
            print(f"\nKnyga '{pavadinimas}' sėkmingai pridėta!")
        else:
            print("\nKlaida pridedant knygą.")

    def rodyti_detalia_statistika(self, paskolintu_knygu_sarasas):
        total_book_count = sum(knyga.pradinis_kiekis for knyga in self.knygu_sarasas)
        borrowed_book_count = sum(len(knygos) for knygos in paskolintu_knygu_sarasas.values())
        available_book_count = total_book_count - borrowed_book_count

        # genre_count = {zanras: kiekis}
        genre_count = {}
        for knyga in self.knygu_sarasas:
            genre_count[knyga.zanras] = genre_count.get(knyga.zanras, 0) + knyga.turimas_kiekis

        # genre_borrow_count = {zanras: kiekis}
        genre_borrow_count = {}
        for knygos in paskolintu_knygu_sarasas.values():
            for item in knygos:
                zanras = item["knyga"].zanras
                genre_borrow_count[zanras] = genre_borrow_count.get(zanras, 0) + 1

        most_popular_genre = max(genre_borrow_count.items(), key=lambda x: x[1], default=("Nėra", 0))
        genre_with_most_books = max(genre_count.items(), key=lambda x: x[1], default=("Nėra", 0))

        reader_borrow_count = {reader_id: len(knygos) for reader_id, knygos in paskolintu_knygu_sarasas.items()}

        now = datetime.now()
        veluojanciu_kiekis = 0

        for skaitytojo_knygos in paskolintu_knygu_sarasas.values():
            for knyga in skaitytojo_knygos:
                grazinimo_data = datetime.strptime(knyga["grąžinimo_data"], "%Y-%m-%d")
                if grazinimo_data < now:
                    veluojanciu_kiekis += 1

        veluojanciu_procentas = (veluojanciu_kiekis / borrowed_book_count * 100) if borrowed_book_count > 0 else 0
        pasiskolintu_procentas = (borrowed_book_count / total_book_count * 100) if total_book_count > 0 else 0


        print("\n=== DETALI BIBLIOTEKOS STATISTIKA ===")
        print(f"Bendras knygų skaičius: {total_book_count}")
        print(f"Pasiskolintos knygos: {borrowed_book_count}")
        print(f"Prieinamos knygos: {available_book_count}")
        print(f"{borrowed_book_count} knygos pasiskolintos iš {total_book_count} galimų knygų. Tai sudaro {pasiskolintu_procentas:.2f}%.")
        print(f"Populiariausias žanras: {most_popular_genre[0]} ({most_popular_genre[1]} kartų pasiskolinta)")
        print(f"Žanras su daugiausia knygų: {genre_with_most_books[0]} ({genre_with_most_books[1]} knygų)")
        print(f"Vėluojančios knygos: {veluojanciu_kiekis}")
        print(f"{veluojanciu_kiekis} knygos vėluoja iš {borrowed_book_count} pasiskolintų knygų. Tai sudaro {veluojanciu_procentas:.2f}%.")

