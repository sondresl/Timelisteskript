# Scipt for å generere timelister for gruppelærere ved UiO

Dette er et personlig prosjekt. Jeg tar ikke ansvar dersom skriptet produserer gale timelister for andre som bruker det. :|

Se `eksempel.csv` for å se et eksempel. Bruk gjerne denne filen som en mal for dine egne timelister.

## Innstallere

For å generere timelisten trenger du tre elementer, som alle må ligge i samme mappe:

- Skriptet
- Blank timeliste
- Inndata (i form av en `.csv` fil)

Det er noen dependencies:
- reportlab (`pip install reportlab`)
- PyPDF2 (`pip install PyPDF2`)
- pandas (`pip install pandas` dersom du ikke har den fra før f.eks gjennom conda)

Skriptet tar syv argumenter, som alle må gis.

Eksempelkjøring:
```bash
python timeliste.py Ola Nordmann IN1000 01-01-2000 August testdata.csv
```

Jeg foreslår og lage et alias som inkluderer alt frem til måneden, så kan den legges inn manult når skriptet kalles.

## Inndata (CSV)

Må ha følgende kolonner:
- timer
- type
- info
- #obliger (Dette er antall obliger rettet)
- oblig#   (Nummer på obligen)
- levering (Hvilket forsøk)

Hvilke kolonner som må fylles inn avhenger av hvilken type det er. Alle typer må ha timeantall, men bare retting vil bruke obliger og leveringsinformasjonen.

Totalt antall timer blir hentet gjennom å summere alle timene. *Det må derfor ikke være en egen rad med summen av alle timene dine i inputfilen.*

Under info er det 7 kategorier (engelske navn for å unngå bruk av æ, ø og å):
- meeting (for gruppelærermøter og evt andre møter)
- lab_prep
- lab
- class_prep
- class
- communication
- other
- oblig (for retting av obliger)

Dersom du skriver samme type info under `annet` så vil skriptet ikke duplisere feltene, men heller summe timene opp til ett felt.

## Notater

Dette prosjektet inneholder en salig blanding av norsk og engelsk. Jeg beklager det, men det er sånn blir.
