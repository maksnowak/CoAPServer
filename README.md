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

Dodatkowo, serwer będzie generował logi ze wszystkimi wydarzeniami, które wystąpiły podczas jego działania

### Niefunkcjonalne

- Biblioteka ma architekturę pozwalającą na łatwą rozbudowę aplikacji o nowe żądania
- Serwer pozwala na jednoczesną obsługę wielu klientów
- Serwer ma poprawnie działać na dowolnej platformie Linux/Unix

## Przypadki użycia

- `GET`: Odczytywanie bieżącej temperatury na czujniku
- `POST`: Zarejestrowanie nowego czujnika
- `PUT`: Aktualizacja temperatury czujnika
- `DELETE`: Usunięcie czujnika

## Analiza sytuacji błędnych

W przypadku wystąpienia sytuacji błędnej, serwer zwróci odpowiedni dla tej sytuacji kod, zgodnie ze specyfikacją [RFC 7252](https://datatracker.ietf.org/doc/html/rfc7252#section-5.9):
- Kod `4.xx` dla błędów po stronie klienta
- Kod `5.xx` dla błędów po stronie serwera

Każdy błąd będzie zapisany w logach do dalszej analizy; rekord będzie zawierał podstawowe informacje, takie jak data i godzina zdarzenia, adres IP klienta, adres URL żądania oraz kod uzyskany w odpowiedzi.

## Środowisko sprzętowo-programowe

- System operacyjny:
  - Ubuntu 24.04
- Konteneryzacja:
  - Docker
  - `docker compose`
- Język programowania:
  - Python 3.11
- Zarządzanie pakietami:
  - `poetry`
- Linter:
  - `ruff`
- Formatter:
  - `ruff`
- Testowanie:
  - `pytest`

## Architektura rozwiązania

Do symulacji architektury rozwiązania zastosujemy Dockera. 
Poszczególne kontenery będą reprezentować elementy architektury, które będą komunikować się za pomocą sieci docekrowej.

## API

## Sposób testowania

- Testy jednostkowe
- Testy integracyjne 
  - poprawność komunikacji klient-serwer
  - stabilność systemu
- Testy manualne, z opisanym ich przebiegiem w dokumentacji końcowej

## Podział prac w zespole

## Przewidywane funkcje do zademonstrowania w ramach odbioru częściowego

- Działająca metoda `GET`
- Działająca metoda `POST`

## Plan pracy z podziałem na tygodnie