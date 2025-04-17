from freezegun import freeze_time
from datetime import datetime
from services.bibliotekos_valdymas import BibliotekosValdymas




# @freeze_time("2025-05-10")
def main():
    print(datetime.now())
    sistema = BibliotekosValdymas()
    sistema.paleidimas()

if __name__ == "__main__":
    main()

