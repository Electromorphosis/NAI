# NAI 6

## Problem Wykrywanie wzroku w celu zwiększania zaangażowania w treści reklamowe

Autor: Paweł Mechliński

Instrukcja użycia:
- Zainstaluj zależności (uwaga, zamiast simpleaudio należy zainstalować complexaudio! Nazwa w imporcie pozostaje ta sama)

Referencje:
- przetrenowane modele:
  - detekcja wzroku: Shameem Hameed (http://umich.edu/~shameem).
  - detekcja twarzy: Rainer Lienhart.
  - Licencje znajdują się w plikach xml.
- dźwięk alarmu: https://www.youtube.com/@mysound1805
- ekran tytułowy wygenerowany za pomocą strony quozio.com
- użyte materiały reklamowe zostały ściągnięte z YouTube, prawa do nich (prawdopodobnie) posiada MediaMarkt.

### Opis Problemu

Powyższy kod rozwiązuje problem monitorowania uwagi użytkownika, szczególnie w kontekście śledzenia otwarcia oczu podczas oglądania materiałów wideo. Problem ten jest istotny w scenariuszach takich jak:

- **Zapobieganie utracie uwagi** lub zaśnięciu podczas oglądania materiałów edukacyjnych lub szkoleń online – kod pomaga w identyfikacji, czy użytkownik przestaje aktywnie obserwować ekran (np. zamyka oczy), i w takim przypadku generuje ostrzeżenie.
- Wsparcie bezpieczeństwa w sytuacjach wymagających czujności – może być użyte w kontekstach, gdzie konieczne jest monitorowanie uwagi operatora, np. w pojazdach autonomicznych lub podczas pracy w niebezpiecznych środowiskach.
- Pomoc w treningu uwagi i koncentracji – narzędzie to może być wykorzystane w programach szkoleniowych, gdzie użytkownicy uczą się utrzymywać uwagę na zadaniach przez określony czas.

Kod ten znajduje zastosowanie w systemach bezpieczeństwa, edukacji, a także w aplikacjach terapeutycznych czy szkoleniowych (i innych), które wymagają śledzenia uwagi użytkownika.