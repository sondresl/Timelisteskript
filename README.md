# Scipt for å generere timelister for gruppelærere ved UiO

## Innstallere

For å generere timelisten trenger du tre elementer, som alle må ligge i samme mappe:

- Skriptet
- Blank timeliste
- Data

Det er noen dependencies:
- reportlab (`pip install reportlab`)
- PyPDF2 (`pip install PyPDF2`)
- pandas (`pip install pandas` dersom du ikke har den fra før gjennom conda)

Skriptet tar syv argumenter, som alle må gis.

Eksempelkjøring:
```bash
python timeliste.py Sondre Lunde IN2040 26-01-1993 August testdata.csv
```

### CSV-filen

Må ha følgende kolonner:
- timer
- type
- info
- #obliger (Dette er antall obliger rettet)
- oblig#   (Nummer på obligen)
- levering (Hvilket forsøk)

Under info er det 7 kategorier:
- meetings (for gruppelærermøter)
- lab_prep
- lab
- class_prep
- class
- kommunikasjon
- annet
- retting
