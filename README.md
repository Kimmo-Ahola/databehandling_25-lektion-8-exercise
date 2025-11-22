# databehandling_25-lektion-7-exercise

## Installation
Först skapar ni en venv som alltid
Sedan måste ni installera relevanta bibliotek i koden
- pip install -r requirements.txt

Implementation av alembic saknar för närvarande. En bra övning är att ni tar bort:
- Base.metadata.drop_all()
- Base.metadata.create_all()

från seeding.py och kör migrationer med alembic istället.

## Övning
Ni har nu en lite större kodbas och tanken är att ni ska lära er att hitta runt i koden.
Klicka runt och försök att förstå strukturen och varför vi vill dela upp kodbasen i olika mappar och filer.

Datan som hamnar i er databas är tagen från en helt slumpmässig källa och ni kommer att märka att det finns en hel del fel i datan.
Detta kallas för "otvättad" data och därför kan vissa datatyper tyckas märkliga. Många kolumner är till exempel i VARCHAR för att hantera detta.