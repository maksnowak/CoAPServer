# PSI Zespół 57 - Serwer CoAP

*Autorzy: Michał Machnikowski, Maksymilian Nowak, Bruno Sienkiewicz*

## Treść zadania

Celem projektu jest implementacja serwera CoAP w języku Python, który będzie obsługiwał przynajmniej żądania `GET`, `POST`, `PUT`, oraz `DELETE`.
Serwer powinien posiadać odpowiednio skonstruowaną architekturę – tak, aby łatwo było dodać nową funkcję obsługującą żądania przychodzące na dany URL.

## Założenia

### Funkcjonalne

- Serwer będzie obsługiwał żądania zgodnie z protokołem CoAP
- Serwer będzie obsługiwał żądania `GET`, `POST`, `PUT`, oraz `DELETE`
- Serwer będzie zwracał odpowiednie kody odpowiedzi
- Serwer będzie generował logi ze wszystkimi zdarzeniami, które wystąpiły podczas jego działania
- Serwer będzie organizował dane w hierachię zasobów, gdzie każdy zasób będzie miał swój unikalny URL
- Serwer będzie pozwalał na obsługę wielu klientów jednocześnie

### Niefunkcjonalne

- Serwer ma architekturę pozwalającą na łatwą rozbudowę aplikacji o nowe żądania
- Serwer pozwala na jednoczesną obsługę wielu klientów bez utraty wydajności
- Serwer ma poprawnie działać na systemie Linux

## Przypadki użycia

Serwer będzie służył do obsługi żądań do sieci urządzeń IoT. Przykładowo, zakładając, że serwer będzie obsługiwał czujniki temperatury, to możliwe przypadki użycia to:

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
- Analiza statyczna:
  - `mypy`
- Testowanie:
  - `pytest`

## Architektura rozwiązania

Do symulacji architektury rozwiązania zastosujemy Dockera.

Poszczególne kontenery będą reprezentować elementy architektury, które będą komunikować się za pomocą sieci docekrowej.

## API

W projekcie planowane są trzy główne bloki funkcjonalne:

- Uruchomienie serwera
- Nasłuchiwanie przychodzących żądań
- Obsługa żądań

## Sposób testowania

- Testy jednostkowe
- Testy integracyjne
  - poprawność komunikacji klient-serwer
  - stabilność systemu
- Testy manualne, z opisanym ich przebiegiem w dokumentacji końcowej

## Podział prac w zespole

- Przygotowanie środowiska – Bruno Sienkiewicz
- Szkielet aplikacji – Bruno Sienkiewicz, Maksymilian Nowak
- Metoda `GET` (+ testy) – Michał Machnikowski
- Metoda `POST` (+ testy) – Maksymilian Nowak
- Metoda `PUT` (+ testy) – Michał Machnikowski
- Metoda `DELETE` (+ testy) – Bruno Sienkiewicz
- Dokumentacja – Michał Machnikowski, Maksymilian Nowak, Bruno Sienkiewicz

## Przewidywane funkcje do zademonstrowania w ramach odbioru częściowego

- Szkielet aplikacji
- Deklaracja każdej z metod (mocki)
- W pełni działająca metoda `GET`

## Plan pracy z podziałem na tygodnie

- 23.12 – 29.12: Przygotowanie środowiska
- 30.12 – 05.01: Stworzenie szkieletu aplikacji
- 06.01 – 12.01: Implementacja metody `GET`
- 13.01 – 19.01: Implementacja pozostałych metod, przygotowanie testów
- 20.01 – 24.01: Weryfikacja poprawności rozwiązania, przygotowanie dokumentacji końcowej

# Instrukcja uruchomienia

- Sklonuj repozytorium:
    ```bash
    git clone https://gitlab-stud.elka.pw.edu.pl/mmachnik/psi-projekt.git
    ```
- Przejdź do katalogu z projektem:
    ```bash
    cd psi-projekt
    ```
- Zainstaluj wszystkie potrzebne zależności:
    ```bash
    make install
    ```
- Uruchom serwer:
    ```bash
    make run
    ```

# Opis najważniejszych struktur i funkcji

## `server.py`

Jest to plik zawierający definicję głównej klasy serwera, `CoAPServer`. Klasa ta przyjmuje jako parametry wejściowe strukturę `routes`, zawierającą informacje o dostępnych zasobach, `host` z adresem IP serwera oraz `port` z numerem portu, na którym serwer ma nasłuchiwać.

Klasa posiada dwie metody - `start()` oraz `shutdown()`. Pierwsza z nich odpowiada za uruchomienie serwera, natomiast druga za jego zatrzymanie.

## `request_handler.py`

Plik ten zawiera definicję klasy `RequestHandler`. W konstruktorze klasy przekazywana jest struktura `routes`, analogicznie do klasy `CoAPServer`. Klasa ta posiada metodę `handle_request()`, przyjmujący jako parametr wejściowy ciąg bajtów reprezentujący żądanie CoAP. Metoda ta zwraca odpowiedź serwera w postaci ciągu bajtów.

Przetworzenie żądania wykorzystuje funkcje `parse_message()` oraz `encode_message()`, które zostaną opisane poniżej.

## `utils/parser.py`

### `parse_message()`

Funkcja ta przyjmuje jako parametr wejściowy ciąg bajtów reprezentujący żądanie CoAP. Funkcja ta zwraca strukturę typu `CoapMessage`, zawierającą informacje o żądaniu.

### `encode_message()`

Funkcja ta przyjmuje jako parametr wejściowy strukturę `CoapMessage`, zawierającą informacje o odpowiedzi serwera. Funkcja ta zwraca ciąg bajtów reprezentujący odpowiedź serwera.

## `utils/construct_response.py`

Plik ten zawiera funkcję `construct_response()`, wykorzystywaną przez konkretne zasoby. Przyjmuje ona żądanie w postaci struktury `CoapMessage`.

# Opis interfejsu użytkownika

# Flagi konfiguracyjne

# Postać logów

# Wykorzystane narzędzia

# Testy