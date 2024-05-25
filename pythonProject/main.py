import pygame
from random import choice

# Ustawienie szerokości i wysokości okna oraz liczby klatek na sekundę
szerokosc, wysokosc = 1200, 700
fps = 8

# Inicjalizacja biblioteki pygame
pygame.init()

# Utworzenie powierzchni o wybranych wymiarach szerokości i wysokości oraz ustawienie zegara
sc = pygame.display.set_mode((szerokosc, wysokosc))
zegar = pygame.time.Clock()

# Ustawienie początkowych współrzędnych oraz rozmiaru komórki labiryntu
x, y = 0, 0
rozmiar = 100

# Obliczenie liczby kolumn i wierszy na podstawie szerokości i wysokości okna oraz rozmiaru komórki
kolumny, wiersze = szerokosc // rozmiar, wysokosc // rozmiar

# Ustawienie szerokości ścian komórek labiryntu oraz definicje kolorów
szerokosc_sciany = 5
kolor_odwiedzonej = pygame.Color('black')
kolor_sciany = pygame.Color('red')
kolor_biezacej_komorki = pygame.Color('white')

# Klasa reprezentująca komórkę labiryntu
class Komorka:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.sciany = {'góra': True, 'lewo': True, 'dół': True, 'prawo': True} # Słownik przechowujący informacje o ścianach komórki
        self.odwiedzona = False

    # Metoda rysująca komórkę
    def rysuj(self):
        x, y = self.x * rozmiar, self.y * rozmiar
        if self.odwiedzona:
            pygame.draw.rect(sc, kolor_odwiedzonej, (x, y, rozmiar, rozmiar))
        if self.sciany['góra']:
            pygame.draw.line(sc, kolor_sciany, (x, y), (x + rozmiar, y), szerokosc_sciany)
        if self.sciany['lewo']:
            pygame.draw.line(sc, kolor_sciany, (x, y), (x, y + rozmiar), szerokosc_sciany)
        if self.sciany['dół']:
            pygame.draw.line(sc, kolor_sciany, (x, y + rozmiar), (x + rozmiar, y + rozmiar), szerokosc_sciany)
        if self.sciany['prawo']:
            pygame.draw.line(sc, kolor_sciany, (x + rozmiar, y), (x + rozmiar, y + rozmiar), szerokosc_sciany)

    # Metoda rysująca bieżącą komórkę
    def rysuj_biezaca_komorke(self):
        x, y = self.x * rozmiar, self.y * rozmiar
        pygame.draw.rect(sc, kolor_biezacej_komorki, (
        x + szerokosc_sciany, y + szerokosc_sciany, rozmiar - szerokosc_sciany, rozmiar - szerokosc_sciany))

    # Metoda sprawdzająca sąsiednie komórki
    def sprawdz_komorke(self, x, y):
        znajdz_indeks = lambda x, y: x + y * kolumny
        if x < 0 or x > kolumny - 1 or y < 0 or y > wiersze - 1:
            return False
        return siatka_komorek[znajdz_indeks(x, y)]

    # Metoda sprawdzająca nieodwiedzone sąsiednie komórki
    def sprawdz_sasiadow(self):
        sasiedzi = []
        gora = self.sprawdz_komorke(self.x, self.y - 1)
        lewo = self.sprawdz_komorke(self.x - 1, self.y)
        dol = self.sprawdz_komorke(self.x, self.y + 1)
        prawo = self.sprawdz_komorke(self.x + 1, self.y)
        if gora and not gora.odwiedzona:
            sasiedzi.append(gora)
        if lewo and not lewo.odwiedzona:
            sasiedzi.append(lewo)
        if dol and not dol.odwiedzona:
            sasiedzi.append(dol)
        if prawo and not prawo.odwiedzona:
            sasiedzi.append(prawo)
        return choice(sasiedzi) if sasiedzi else False

# Funkcja usuwająca ściany pomiędzy bieżącą komórką a następną
def usun_sciany(biezaca, nastepna):
    dx, dy = biezaca.x - nastepna.x, biezaca.y - nastepna.y
    if dx == 1:
        biezaca.sciany['lewo'] = False
        nastepna.sciany['prawo'] = False
    if dx == -1:
        biezaca.sciany['prawo'] = False
        nastepna.sciany['lewo'] = False
    if dy == 1:
        biezaca.sciany['góra'] = False
        nastepna.sciany['dół'] = False
    if dy == -1:
        biezaca.sciany['dół'] = False
        nastepna.sciany['góra'] = False

# Utworzenie siatki komórek labiryntu
siatka_komorek = [Komorka(kolumna, wiersz) for wiersz in range(wiersze) for kolumna in range(kolumny)]
biezaca_komorka = siatka_komorek[0] # Ustawienie początkowej komórki na lewym górnym rogu
stos = [] # Inicjalizacja stosu do śledzenia ścieżki

while True:
    sc.fill(pygame.Color("darkblue")) # Wypełnienie ekranu kolorem ciemnoniebieskim

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # Rysowanie wszystkich komórek siatki
    [komorka.rysuj() for komorka in siatka_komorek]

    # Oznaczenie bieżącej komórki jako odwiedzonej i jej zaznaczenie na ekranie
    biezaca_komorka.odwiedzona = True
    biezaca_komorka.rysuj_biezaca_komorke()

    # Sprawdzenie sąsiadów bieżącej komórki
    nastepna_komorka = biezaca_komorka.sprawdz_sasiadow()
    if nastepna_komorka:
        nastepna_komorka.odwiedzona = True
        stos.append(biezaca_komorka)
        usun_sciany(biezaca_komorka, nastepna_komorka)
        biezaca_komorka = nastepna_komorka
    elif stos:
        biezaca_komorka = stos.pop()

    pygame.display.flip() # Odświeżenie ekranu
    zegar.tick(fps) # Ustawienie liczby klatek na sekundę