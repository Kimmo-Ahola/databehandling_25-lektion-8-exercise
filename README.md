# Instruktioner

## Installation
Först skapar ni en venv som alltid

Sedan måste ni installera relevanta bibliotek i koden
- pip install -r requirements.txt

Glöm inte att ändra connection string i db.py till er egen och se till att databasen är skapad innan ni kör.

Efter att ni har kört en seeding och fått in databasen kan ni kommentera bort raden
Seeding.create_movie_database() från main.py

## Om repot
Ni har nu en lite större kodbas och tanken är att ni ska lära er att hitta runt i koden.
Klicka runt och försök att förstå strukturen och varför vi vill dela upp kodbasen i olika mappar och filer.

Datan som hamnar i er databas är tagen från en helt slumpmässig källa och ni kommer att märka att det finns en hel del fel i datan.
Detta kallas för "otvättad" data och därför kan vissa datatyper tyckas märkliga. Många kolumner är till exempel i VARCHAR för att hantera detta.
Att "tvätta" data är en stor del av dataanalys men ingår inte i den här kursens omfång. Ni kommer dock att behöva hantera NULL/None i er Python-kod för att undvika att programmet kraschar.


Fokus är såklart på att ni ska skriva queries med SQLAlchemy men ni bör också skriva samma queries i MySQL för att öva på det också. Dubbelkolla gärna att ni får samma svar.

> OBS! Vissa frågor ber er att uppdatera kolumner. Detta behöver ni endast göra i Python. Tänk också på att Base.metadata.drop_all() samt Base.metadata.create_all() skriver över era uppdateringar. Byt därför helst till alembic.

## Övningar för querying
Övningar för querying med SQLAlchemy. Skapa en funktion för varje fråga och kalla på dessa i main.py. Till exempel: 

```python
from sqlalchemy.orm import Session
def Q_1(session: Session):
	res = session.query()...
		
def Q_2(session: Session):
	with ...
```
Använd gärna type hints när ni returnerar från en funktion

```Python
from sqlalchemy.orm import Session, Query
from typing import List
def example(session: Session) -> List[Actor]:
	query: Query[Actor] = session.query(Actor)

	return query.all()
```


Ni väljer själva om ni skapar en konsolmeny för detta (bra övning) eller bara kommenterar bort tidigare funktionsanrop.

> Många av frågorna nedan kräver joins.
>
> Vissa frågor kräver funktioner. Ni hittar dessa under sqlalchemy func (from sqlalchemy import func)


1. Det finns en film som saknar längd. Hitta denna film och uppdatera värdet till det korrekta (2h 29m)
1. Hitta alla skådespelare som saknar efternamn.
	1. Skriv också ut hur många de är till antalet på en ny rad.
1. Hur många filmer finns det som har genren "Action"?
	1. Skriv ut alla dessa filmer
1. Hur många filmer finns det som har över 8.1 i betyg?
1. gross_worldwide innehåller felaktig data. Skriv en funktion som hämtar alla rader som inte börjar med ett "$" och sätt dessa världen till NULL/None
1. Hur många filmer finns det som är gjorda mellan 1959 och 1970 (båda årtalen är inclusive)
1. Lista alla filmer som börjar med "The". Skriv ut antalet också på en ny rad.
1. Lista alla filmer som har språk på Persiska.
1. Lista alla filmer utan vinster (utan wins/win)
1. Lista alla filmer som har vunnit minst 1 oscar
1. Lista alla skådespelare och deras roller som har varit med i den högst rankade filmen
1. Lista alla filmer som har Disney som produktionsbolag
1. Vilka filmer har Chung Seo-kyung varit involverad i som en writer?
1. Hur många writers finns det som har ett full_name som innehåller minst två st 'a'?
1. Vilka filmer har writers i frågan ovan varit medverkande i? 
1. Lista alla filmer som har minst en siffra i sitt namn. Lista också skådespelarna som är med i den första filmen (två separata queries)
1. Lista alla filmer som har varit med i topp #50. Lista också skådespelarna som är med i den första filmen (två separata queries)
1. Lista alla filmer som har en storyline relaterat till police
1. Lista alla filmer som har en storyline relaterat till police och skriv ut vilken Genre de tillhör.
1. Lista alla filmer som saknar en Genre (tips: left join)
1. Lista alla filmer som saknar en Writer
1. Uppdatera följande filmer så att de har svenska som originalspråk: Persona, The Seventh Seal, Wild Strawberries

Svårare frågor
1. Finns det några filmer som heter ungefär samma sak? (Tips: kolla om de har samma tecken i början av titeln)
1. Lista alla roller i cast som har minst 2 st av samma namn, dvs finns det filmer där kolumnen role är identisk?
1. Lägg till en ny kolumn "duration_in_minutes" och skriv en funktion som räknar om h och m till från kolumnen length till en int (nu kan vi sortera korrekt)
1. Skriv en funktion som går igenom budget-kolumnen och sorterar bort alla icke-amerikanska värden (inga dollartecken i början). Ta sedan bort dollartecknet och alla tecken som inte är siffor från samtliga rader som har värden. (Gör detta i flera steg och dubbelkolla mellan)
1. Gör samma sak som frågan ovan fast för gross_worldwide.
1. Efter ni har gjort de två frågorna ovan kan ni ändra datatyp på kolumnen med alembic till float/decimal och utföra aritmetik.. Se till att Base.drop_all(engine) är bortttagen.
1. Räkna ut filmernas vinstfaktor (gross/budget) och sortera i fallande ordning.
1. Gruppera alla filmer enligt originalspråk.
1. Gruppera alla filmer enligt originalspråk men ta denna bort gång Null/None samt unknown.
1. Vilket produktionsbolag har flest filmer i topplistan?
1. Vilket år har flest filmer i topplistan?
	1. Skriv ut alla dessa filmer
1. Vilken skådespelare har flest antal 'a' i sitt full_name? (Hint: använd Length samt replace)
1. Testa samma fråga som övan fast med 'ö'. Får du konstiga svar i MySQL? (Hint: använd char_length istället för length)

Subqueries (Extra svåra!!)
1. Visa den film som har kortast titel
1. Visa den film som har längst titel



## Övningar för databasmodellering

<img width="991" height="898" alt="image" src="https://github.com/user-attachments/assets/6eaf91f0-4851-4676-93c6-19b7aa0cb834" />

1. Det saknas tabeller för origin_countries.
> Relationen mellan movies och origin countries är many-to-many. Ni kan hitta inspiration från production_company.py
> Vid seeding kan ni kolla hur production companies seedas i seeding.py-filen
2. Lägg till en ny tabell för en användare samt för recensioner. Recensionerna ska inte påverka Score som finns i Movies utan vara separat från denna.
> Enkla varianten: En film kan ha en recension. En användare kan recensera flera filmer. (One-to-Many)
> 
> Svårare varianten: En film kan kan många recensioner från flera envändare. En användare kan recensera flera filmer. (Many-to-Many)


## Fler övningar?

Klistra in samtliga modeller till chatgpt/claude/ai och be om MySQL-frågor. Var specifika om ni vill ha nybörjarfrågor (räcker gott och väl till denna kurs) eller svårare frågor.
