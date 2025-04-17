from services.file_manager import FileHandler
from datetime import datetime, timedelta


class Skaitytojas:
    def __init__(self):
        self.paskolintu_knygu_failas = "C:\\Users\\djfkj\\Desktop\\python_pagrindai\\atsiskaitymas123\\atsiskaitymas_project\\sarasai\\paskolintos_knygos.pkl"
        self.skaitytoju_saraso_failas = "C:\\Users\\djfkj\\Desktop\\python_pagrindai\\atsiskaitymas123\\atsiskaitymas_project\\sarasai\\skaitytoju_sarasas.pkl"
        self.skaitytoju_sarasas = FileHandler.read_from_pickle(self.skaitytoju_saraso_failas, [])
        self.paskolintu_knygu_sarasas = FileHandler.read_from_pickle(self.paskolintu_knygu_failas, {})
        
    def autentifikuoti(self, skaitytojo_id):
        return skaitytojo_id in self.skaitytoju_sarasas
    
    def sukurti_nauja_skaitytoja(self):
        naujas_id = max(self.skaitytoju_sarasas) + 1 if self.skaitytoju_sarasas else 1000
        self.skaitytoju_sarasas.append(naujas_id)
        self.paskolintu_knygu_sarasas[naujas_id] = []
        FileHandler.write_to_pickle(self.skaitytoju_saraso_failas, self.skaitytoju_sarasas)
        FileHandler.write_to_pickle(self.paskolintu_knygu_failas, self.paskolintu_knygu_sarasas)
        return naujas_id

    def pasiskolinti_knyga_logic(self, skaitytojo_id, knyga):
        if skaitytojo_id in self.paskolintu_knygu_sarasas:
            dabar = datetime.now()
            for item in self.paskolintu_knygu_sarasas[skaitytojo_id]:
                grąžinimo_data = datetime.strptime(item["grąžinimo_data"], "%Y-%m-%d")
                if dabar > grąžinimo_data:
                    print("\nNegalite pasiskolinti naujų knygų, kol turite vėluojančių knygų.")
                    return False

            if len(self.paskolintu_knygu_sarasas[skaitytojo_id]) >= 3:
                print("\nNegalite pasiskolinti daugiau nei 3 knygų vienu metu.")
                return False

            if knyga.turimas_kiekis <= 0:
                print(f"\nAtsiprašome, knygos '{knyga.pavadinimas}' šiuo metu nėra.")
                return False

            grąžinimo_data = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
            self.paskolintu_knygu_sarasas[skaitytojo_id].append({
                "knyga": knyga,
                "grąžinimo_data": grąžinimo_data
            })
            FileHandler.write_to_pickle(self.paskolintu_knygu_failas, self.paskolintu_knygu_sarasas)
            print(f"\nKnyga '{knyga.pavadinimas}' sėkmingai pasiskolinta! Grąžinimo data: {grąžinimo_data}")
            return True
        else:
            print(f"\nKlaida: skaitytojo ID {skaitytojo_id} nerastas.")
            return False
        
    def tikrinti_terminus(self, skaitytojo_id):
        dabar = datetime.now()
        if skaitytojo_id in self.paskolintu_knygu_sarasas:
            print("\n=== VĖLUOJANČIOS KNYGOS ===")
            yra_veluojanciu = False
            for item in self.paskolintu_knygu_sarasas[skaitytojo_id]:
                grąžinimo_data = datetime.strptime(item["grąžinimo_data"], "%Y-%m-%d")
                if dabar > grąžinimo_data:
                    yra_veluojanciu = True
                    print(f"Knyga: {item['knyga'].pavadinimas} (autorius: {item['knyga'].autorius})")
                    print(f"Grąžinimo data: {item['grąžinimo_data']}")
                    print("-" * 40)
            if not yra_veluojanciu:
                print("\nNeturite vėluojančių knygų.")
        else:
            print("\nNeturite pasiskolintų knygų.")

    def patikrinti_ar_turi_veluojanciu_knygu(self, skaitytojo_id):
        dabar = datetime.now()
        if skaitytojo_id in self.paskolintu_knygu_sarasas:
            for item in self.paskolintu_knygu_sarasas[skaitytojo_id]:
                grąžinimo_data = datetime.strptime(item["grąžinimo_data"], "%Y-%m-%d")
                if dabar > grąžinimo_data:
                    return True
        return False
    
    def perziureti_veluojancias_knygas(self):
        print("\n=== VĖLUOJANČIOS KNYGOS ===")
        dabar = datetime.now()
        yra_veluojanciu = False

        for skaitytojo_id, knygos in self.paskolintu_knygu_sarasas.items():
            if self.patikrinti_ar_turi_veluojanciu_knygu(skaitytojo_id):
                yra_veluojanciu = True
                for item in knygos:
                    grąžinimo_data = datetime.strptime(item["grąžinimo_data"], "%Y-%m-%d")
                    if dabar > grąžinimo_data:
                        print(f"Skaitytojo ID: {skaitytojo_id}")
                        print(f"  Knyga: {item['knyga'].pavadinimas} (autorius: {item['knyga'].autorius})")
                        print(f"  Grąžinimo data: {item['grąžinimo_data']}")
                        print("-" * 40)

        if not yra_veluojanciu:
            print("\nNėra vėluojančių knygų.")

