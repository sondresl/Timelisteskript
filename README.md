# Scipt for å generere timelister for gruppelærere ved UiO

Dette er et personlig prosjekt. Jeg tar ikke ansvar dersom skriptet produserer gale timelister for andre som bruker det.

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

## Inndata (CSV)

Må ha følgende kolonner:
- timer
- type
- info
- #obliger (Dette er antall obliger rettet)
- oblig#   (Nummer på obligen)
- levering (Hvilket forsøk)

Alle andre kolonner er valgfrie, og vil bli ignorert av skriptet.

Totalt antall timer blir hentet gjennom å summere alle timene. *Det må derfor ikke være en egen rad med summen av alle timene dine i regnearket.*

Under info er det 7 kategorier:
- meetings (for gruppelærermøter og evt andre møter)
- lab_prep
- lab
- class_prep
- class
- kommunikasjon
- annet
- retting
