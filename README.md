# PSI Serwer CoAP

## Treść zadania

Celem projektu jest implementacja serwera CoAP, który będzie obsługiwał przynajmniej żądania `GET`, `POST`, `PUT`, oraz `DELETE`.
Serwer powinien posiadać odpowiednio skonstruowaną architekturę - tak, aby łatwo było dodać nową funkcję obsługującą żądania przychodzące na dany URL.

Planujemy stworzyć moduł do systemu kontroli temperatury, który będzie realizował komunikację między czujnikami i centralnym serwerem.

## Założenia

### Funkcjonalne

Nasza biblioteka będzie umożliwiała następujące funkcje:
- Dodawanie czujników
- Usuwanie czujników
- Modyfikacja statusu czujników
- Pobranie odczytów temperatur

### Niefunkcjonalne

## Przypadki użycia

GET: Odczytywanie bieżącej temperatury na czujniku
POST: Zarejestrowanie nowego czujnika
PUT: Aktualizacja temperatury czujnika
DELETE: Usunięcie czujnika

## Analiza sytuacji błędnych

## Środowisko sprzętowo-programowe

- System operacyjny:
  - Ubuntu 24.04
- Konteneryzacja:
  - Docker
  - docker compose
- Język programowania:
  - Python 3.11
- Zarządzanie pakietami:
  - poetry
- Linter:
  - ruff
- Formatter:
  - ruff
- Testowanie:
  - pytest

## Architektura rozwiązania

Do symulacji architektury rozwiązania zastosujemy Dockera. 
Poszczególne kontenery będą reprezentować elementy architektury, które będą komunikować się za pomocą sieci docekrowej.

## API

## Sposób testowania

- Testy jednostkowe
- Testy integracyjne 
  - poprawność komunikacji klient-serwer
  - stabilność systemu

## Podział prac w zespole

## Przewidywane funkcje do zademonstrowania w ramach odbioru częściowego

## Plan pracy z podziałem na tygodnie