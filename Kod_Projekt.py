MAX, MIN = 1000, -1000

class NumerickiKrizicKruzic:
    def __init__(self, depth):
        self.ploca = [[' ' for _ in range(3)] for _ in range(3)]
        self.dostupni_brojevi = set(range(1, 10))
        self.igrac = True  # True za ljudskog igraca, False za AI
        self.max_depth = depth

    def prikaz_ploce(self):
        print("\nTrenutno stanje ploče:")
        for red in self.ploca:
            print("| " + " | ".join(str(polje) if polje != ' ' else ' ' for polje in red) + " |")
            print("-" * 13)
        print()

    def pobjednik(self):
        linije = []
        linije.extend(self.ploca)
        linije.extend([[self.ploca[r][s] for r in range(3)] for s in range(3)])
        linije.append([self.ploca[i][i] for i in range(3)])
        linije.append([self.ploca[i][2 - i] for i in range(3)])

        for linija in linije:
            brojevi = [bro for bro in linija if bro != ' ']
            if len(brojevi) == 3 and sum(brojevi) == 15:
                return True
        return False

    def izjednaceno(self):
        return all(self.ploca[i][j] != ' ' for i in range(3) for j in range(3))

    def napravi_potez(self, red, stupac, broj):
        if 0 <= red < 3 and 0 <= stupac < 3:
            if self.ploca[red][stupac] == ' ' and broj in self.dostupni_brojevi:
                self.ploca[red][stupac] = broj
                self.dostupni_brojevi.remove(broj)
                return True
            else:
                print("To polje je već zauzeto ili broj nije dostupan.")
        else:
            print("Koordinate su izvan granica ploče. Pokušajte ponovo.")
        return False

    def pregled_ploce(self):
        if self.pobjednik():
            return 100 if not self.igrac else -100
        return 0

    def heuristicka_procjena(self):
        rezultat = 0
        linije = self.ploca + [[self.ploca[r][s] for r in range(3)] for s in range(3)] \
                + [[self.ploca[i][i] for i in range(3)]] + [[self.ploca[i][2 - i] for i in range(3)]]

        for linija in linije:
            iskoristeni_brojevi = [bro for bro in linija if bro != ' ']
            linija_sum = sum(iskoristeni_brojevi)
            if len(iskoristeni_brojevi) == 2 and linija_sum < 15:
                rezultat += (15 - linija_sum)  
            elif len(iskoristeni_brojevi) == 3 and linija_sum == 15:
                return 100 if not self.igrac else -100  

        return rezultat

    def minimax(self, depth, is_maximizing, alpha, beta):
        rezultat = self.pregled_ploce()
        if rezultat == 100 or rezultat == -100 or self.izjednaceno():
            return rezultat

        if depth == self.max_depth:
            return self.heuristicka_procjena()

        if is_maximizing:
            bestVal = MIN
            for i in range(3):
                for j in range(3):
                    if self.ploca[i][j] == ' ':
                        for bro in [n for n in self.dostupni_brojevi if n % 2 == 0]:
                            self.ploca[i][j] = bro
                            self.dostupni_brojevi.remove(bro)
                            value = self.minimax(depth + 1, False, alpha, beta)
                            self.ploca[i][j] = ' '
                            self.dostupni_brojevi.add(bro)
                            bestVal = max(bestVal, value)
                            alpha = max(alpha, value)
                            if beta <= alpha:
                                break
            return bestVal
        else:
            bestVal = MAX
            for i in range(3):
                for j in range(3):
                    if self.ploca[i][j] == ' ':
                        for bro in [n for n in self.dostupni_brojevi if n % 2 != 0]:
                            self.ploca[i][j] = bro
                            self.dostupni_brojevi.remove(bro)
                            value = self.minimax(depth + 1, True, alpha, beta)
                            self.ploca[i][j] = ' '
                            self.dostupni_brojevi.add(bro)
                            bestVal = min(bestVal, value)
                            beta = min(beta, value)
                            if beta <= alpha:
                                break
            return bestVal

    def potez_ai(self):
        naj_rezultat = MIN
        naj_potez = None
        naj_broj = None
        for i in range(3):
            for j in range(3):
                if self.ploca[i][j] == ' ':
                    for bro in [n for n in self.dostupni_brojevi if n % 2 == 0]:
                        self.ploca[i][j] = bro
                        self.dostupni_brojevi.remove(bro)
                        rezultat = self.minimax(0, False, MIN, MAX)
                        self.ploca[i][j] = ' '
                        self.dostupni_brojevi.add(bro)
                        if rezultat > naj_rezultat:
                            naj_rezultat = rezultat
                            naj_potez = (i, j)
                            naj_broj = bro
        if naj_potez and naj_broj:
            self.napravi_potez(naj_potez[0], naj_potez[1], naj_broj)
            print(f"AI postavlja broj {naj_broj} na poziciju {naj_potez[0] + 1}, {naj_potez[1] + 1}")

    def pocetak_igre(self):
        print("Dobrodošli u Numerički križić kružić!")
        print("Igra se na ploči 3x3. Cilj je dobiti zbroj 15 u redu, stupcu ili dijagonali.")
        print("Vi ste igrač i igrate s neparnim brojevima (1, 3, 5, 7, 9). AI koristi parne brojeve (2, 4, 6, 8).")

        while True:
            self.ploca = [[' ' for _ in range(3)] for _ in range(3)]
            self.dostupni_brojevi = set(range(1, 10))
            self.igrac = True
            self.prikaz_ploce()

            while True:
                if self.igrac:
                    print(f"Dostupni brojevi za igrača: {[n for n in self.dostupni_brojevi if n % 2 == 1]}")
                    try:
                        red, stupac = map(int, input("Unesite koordinate (redak i stupac, npr. 1 2): ").split())
                        broj = int(input("Odaberite broj: "))
                        red -= 1
                        stupac -= 1
                        if (broj % 2 == 1 and self.napravi_potez(red, stupac, broj)):
                            self.igrac = False
                        else:
                            continue
                    except ValueError:
                        print("Unos nije ispravan. Unesite brojeve za redak, stupac i odabrani broj.")
                        continue
                else:
                    print("AI je na potezu...")
                    self.potez_ai()
                    self.igrac = True

                self.prikaz_ploce()

                if self.pobjednik():
                    if self.igrac:
                        print("AI je pobijedio!")
                    else:
                        print("Čestitamo! Pobijedili ste!")
                    break
                elif self.izjednaceno():
                    print("Neriješeno!")
                    break

            play_again = input("Želite li igrati ponovo? (da/ne): ").strip().lower()
            if play_again != 'da':
                print("Hvala što ste igrali! Doviđenja.")
                break

class ObicniKrizicKruzic:
    def __init__(self, depth):
        self.ploca = [[' ' for _ in range(3)] for _ in range(3)]
        self.igrac = True
        self.max_depth = depth

    def prikaz_ploce(self):
        print("\nTrenutno stanje ploče:")
        for red in self.ploca:
            print("| " + " | ".join(red) + " |")
            print("-" * 13)

    def pobjednik(self):
        linije = []
        linije.extend(self.ploca)
        linije.extend([[self.ploca[r][s] for r in range(3)] for s in range(3)])
        linije.append([self.ploca[i][i] for i in range(3)])
        linije.append([self.ploca[i][2 - i] for i in range(3)])

        for linija in linije:
            if len(set(linija)) == 1 and linija[0] != ' ':
                return True
        return False

    def izjednaceno(self):
        return all(self.ploca[i][j] != ' ' for i in range(3) for j in range(3))

    def napravi_potez(self, red, stupac, znak):
        if 0 <= red < 3 and 0 <= stupac < 3:
            if self.ploca[red][stupac] == ' ':
                self.ploca[red][stupac] = znak
                return True
            else:
                print("To polje je već zauzeto.")
        else:
            print("Koordinate su izvan granica ploče. Pokušajte ponovo.")
        return False

    def pregled_ploce(self):
        if self.pobjednik():
            return 100 if not self.igrac else -100
        return 0

    def heuristicka_procjena(self):
        rezultat = 0
        linije = self.ploca + [[self.ploca[r][s] for r in range(3)] for s in range(3)] \
            + [[self.ploca[i][i] for i in range(3)]] + [[self.ploca[i][2 - i] for i in range(3)]]

        for linija in linije:
            if linija.count('O') > 0 and linija.count('X') == 0:
                rezultat += linija.count('O')
            if linija.count('X') > 0 and linija.count('O') == 0:
               rezultat -= linija.count('X')
        
        return rezultat

    def minimax(self, depth, is_maximizing, alpha, beta):
        rezultat = self.pregled_ploce()
        if rezultat == 100 or rezultat == -100 or self.izjednaceno():
            return rezultat

        if depth == self.max_depth:  # Maksimalna dubina za pretraživanje
            return self.heuristicka_procjena()

        if is_maximizing:
            bestVal = MIN
            for i in range(3):
                for j in range(3):
                    if self.ploca[i][j] == ' ':
                        self.ploca[i][j] = 'O'
                        value = self.minimax(depth + 1, False, alpha, beta)
                        self.ploca[i][j] = ' '
                        bestVal = max(bestVal, value)
                        alpha = max(alpha, value)
                        if beta <= alpha:
                            break
            return bestVal
        else:
            bestVal = MAX
            for i in range(3):
                for j in range(3):
                    if self.ploca[i][j] == ' ':
                        self.ploca[i][j] = 'X'
                        value = self.minimax(depth + 1, True, alpha, beta)
                        self.ploca[i][j] = ' '
                        bestVal = min(bestVal, value)
                        beta = min(beta, value)
                        if beta <= alpha:
                            break
            return bestVal

    def potez_ai(self):
        naj_rezultat = MIN
        najbolji_potez = None
        for i in range(3):
            for j in range(3):
                if self.ploca[i][j] == ' ':
                    self.ploca[i][j] = 'O'
                    rezultat = self.minimax(0, False, MIN, MAX)
                    self.ploca[i][j] = ' '
                    if rezultat > naj_rezultat:
                        naj_rezultat = rezultat
                        najbolji_potez = (i, j)
        if najbolji_potez:
            self.napravi_potez(najbolji_potez[0], najbolji_potez[1], 'O')
            print(f"AI postavlja 'O' na poziciju {najbolji_potez[0] + 1}, {najbolji_potez[1] + 1}")

    def pocetak_igre(self):
        print("Dobrodošli u Križić-Kružić!")
        print("Igra se na ploči 3x3. Cilj je spojiti 3 znaka u redu, stupcu ili dijagonali.")

        while True:
            self.ploca = [[' ' for _ in range(3)] for _ in range(3)]
            self.igrac = True
            self.prikaz_ploce()

            while True:
                if self.igrac:
                    try:
                        red, stupac = map(int, input("Unesite koordinate (redak i stupac, npr. 1 2): ").split())
                        red -= 1
                        stupac -= 1
                        if self.napravi_potez(red, stupac, 'X'):
                            self.igrac = False
                        else:
                            continue
                    except ValueError:
                        print("Unos nije ispravan. Unesite brojeve za redak i stupac.")
                        continue
                else:
                    print("AI je na potezu...")
                    self.potez_ai()
                    self.igrac = True

                self.prikaz_ploce()

                if self.pobjednik():
                    if self.igrac:
                        print("AI je pobijedio!")
                    else:
                        print("Čestitamo! Pobijedili ste!")
                    break
                elif self.izjednaceno():
                    print("Neriješeno!")
                    break

            play_again = input("Želite li igrati ponovo? (da/ne): ").strip().lower()
            if play_again != 'da':
                print("Hvala što ste igrali! Doviđenja.")
                break



def pokreni_igru():
    print("Dobrodošli! Odaberite igru koju želite igrati:")
    print("1. Obični Križić-Kružić")
    print("2. Numerički Križić-Kružić")

    while True:
        izbor = input("Unesite 1 ili 2 za odabir igre: ").strip()
        if izbor == '1':
            while True:
                try:
                    depth = int(input("Unesite dubinu pretraživanja za AI (npr. 2, 3, 4): "))
                    if depth > 0:
                        igra = ObicniKrizicKruzic(depth)
                        igra.pocetak_igre()
                        return
                    else:
                        print("Dubina mora biti pozitivan broj.")
                except ValueError:
                    print("Unesite ispravan broj za dubinu pretraživanja.")

        elif izbor == '2':
            while True:
                try:
                    depth = int(input("Unesite dubinu pretraživanja za AI (npr. 2, 3, 4): "))
                    if depth > 0:
                        igra = NumerickiKrizicKruzic(depth)
                        igra.pocetak_igre()
                        return
                    else:
                        print("Dubina mora biti pozitivan broj.")
                except ValueError:
                    print("Unesite ispravan broj za dubinu pretraživanja.")
        else:
            print("Neispravan unos. Odaberite 1 ili 2.")

pokreni_igru()
