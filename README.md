# Transrel_EEG
Łatwy wariant transrela z 1 wskazówką u góry


Prezentacja pary bodźców (na przykładach oznaczam je symbolicznie A i B) przedzielonych znakiem / albo \ (np. A\B) i czterech odpowiedzi, z których:
* odpowiedź 1 zawiera te same bodźce z przeciwnym znakiem (np. A/B)
* odpowiedź 2 zawiera odwrócone bodźce z tym samym znakiem (B\A)
* odpowiedź 3 zawiera te same bodźce przedzielone | (A|B)
* odpowiedź 4 zawiera zależnie od warunku:

- warunek łatwy: tę samą parę (A\B)
- warunek trudny: odwróconą parę z przeciwnym znakiem (B/A)

Dodatkowo, jest warunek kontrolny, w którym prezentowane jest A|B. 

W warunku łatwym i trudnym poprawna jest odpowiedź 4, a w warunku kontrolnym poprawna jest odpowiedź 3. Oczywiście kolejność odpowiedzi na ekranie jest losowa, a za A i B można podstawić dowolne bodźce. 

Reaguje się klawiszami numerycznymi 1, 2, 3, enter (czterema palcami jednej ręki) w kolejności odpowiadającej kolejności odpowiedzi na ekranie. Bodźcami będą 4 figury geometryczne: koło, kwadrat, trapez, sześciokąt. Czyli wygląda to np. tak (warunek trudny):
```
           ⌂/□


  ⌂\□       □\⌂        ⌂|□       □/⌂

   1         2          3       enter
```
Losowo sekwencja 25 warunków łatwych, 25 trudnych i 25 kontrolnych. Czas prezentacji trzeba będzie dobrać, żeby zadanie dawało odpowiednią trudność w warunku trudnym (~50%), ale na początek można dać 10 s.


## TODO:
* Tests