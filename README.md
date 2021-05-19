# Stads
The python class `Stads` in `Stads.py` is a simple interface for automated (without manually logging in) lookup of student grades in Stads given the student id (studienummer). Here is a simple example of the use:
```
from Stads import Stads

userid = 'youruserid'
password = 'yourpassword'
studentid = 'studentid'

st = Stads(userid, password, ikkeaktive=True)

lookup = st.getKarakterer(studentid)

for stadskode, kursusnavn, karakter, dato in lookup:
    print(stadskode, kursusnavn, karakter, dato)
```

The function `getKarakterer` (above) returns a list of tuples given the student id (studienummer/årskortnummer) as a string. Each tuple is a tuple of four strings:
```
(stadskode, kursusnavn, karakter, dato).
```
The list comprises a complete roster of the student's grades.

## Requirements

The code depends heavily on the Selenium library: https://github.com/SeleniumHQ/Selenium for automated browsing.

You need to have the following python3 libraries installed:

- Selenium: `pip3 install selenium`
- BeautifulSoup: `pip3 install beautifulsoup4`

Updated versions of drivers for web engines in `/usr/local/bin` (below I have listed the ones for `Chrome` and `Firefox`):

- chromedriver: https://sites.google.com/a/chromium.org/chromedriver/ (place fex at `/usr/local/bin/chromedriver`)
- geckodriver: https://github.com/mozilla/geckodriver/releases

## Stadskoder

Here is a sample of codes for courses (kursuskoder) in Stads:

```
55007Q0002: Matematisk Analyse 1 (gammel ordning, 5 ECTS)
55003Q0005: Matematisk Analyse 2 (gammel ordning, 5 ECTS)
550171E002: Matematisk Analyse 1 (10 ECTS)
550171E005: Matematisk Analyse 2 (10 ECTS)
55003Q0006: Lineær algebra
55003Q0019: Algebra 
55003Q0021: Geometri
550171E008: Målteori (10 ECTS)
55003Q0010: Målteori (gammel ordning, 5 ECTS)
550121E001: Reel analyse og sandsynlighedsteori (gammel ordning, 5 ECTS)
55003Q0020: Differentialligninger
55003Q0017: Kompleks funktionsteori
```
