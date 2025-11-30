# Koiratietokanta

Tietokannat & web-ohjelmoinnit 2025 kurssi.


🐾 Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.


🐾 Käyttäjä pystyy lisäämään sovellukseen koiran, antamaan sille nimen, rodun ja iän. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään tietoja.


🐾 Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät koirat.


🐾 Käyttäjä pystyy etsimään tietoa koirista hakusanoilla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä ilmoituksia.


🐾 Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja kuten kuinka monta koiraa omistaa ja niiden tiedot sekä kuinka monta kertaa on jättänyt ilmoituksen.


🐾 Käyttäjä pystyy valitsemaan koirallensa yhden tai useamman luokan, kuten onko koira minkä kokoinen tai millainen sen luonne on. Mahdolliset luokat ovat tietokannassa.


🐾 Sovelluksessa on pääasiallisen tietokohteen lisäksi toissijainen tietokohde, jossa pystyy kertomaan enemmän koirastaan, esim. etsii seuraa agilityyn, lenkeille, kisoihin, koirapuistoon, tarvitsee välillä ulkoiluttajaa.



<h1>Miten sovellusta voi käyttää?</h1>

🐾 Kopioi projektin linkki oikealta ylhäältä painamalla vihreätä Code-nappia > SSH > ota linkki talteen Clonesta tai;
```bash
git@github.com:emmapiittala/koiratietokanta.git
```

🐾 Avaa komentorivi ja kloonaa projekti komennolla: git clone sekä perään linkki. 
Näin sinulle pitäisi asentua koiratietokanta-projektini. 
```bash 
git clone git@github.com:emmapiittala/koiratietokanta.git
```

🐾 Mene koiratietokanta projektiin ja aktivoi virtuaaliympäristö komennolla: 
```bash
source venv/bin/activate
```

🐾 Asenna pythoniin kirjasto:
 ```bash
pip install flask
```
🐾 Luo tietokanta lisäämällä komentoriville: 
```bash
sqlite3 database.db < schema.sql
```

🐾 Kirjoita komentoriville: flask run <br>
Komentoriville pitäisi nyt ilmestyä linkki, joka on suunnilleen tämän näköinen: (http://127.0.0.1:5000). Ota linkki talteen ja siirry selaimeen. 
```bash
flask run
```

🐾 Liitettyä linkin selaimeen, pääset koiratietokannan nettisivuille. Tässä versiossa pystyt luomaan tunnuksen, kirjautumaan sisään, etsimään ilmoituksia sekä vain kirjautuneet käyttäjät pystyvät myös luomaan ilmoituksia sekä ilmoituksen jättänyt pystyy poistamaan ilmoituksensa. 


‼️‼️‼️EDIT 1.12. Sovelluksessa on käyttäjäsivut ja siellä näkyy käyttäjän lisäämät kohteet. Käyttäjä pystyy valitsemaann useamman luokittelun. Sain vaan niin juntturaan etten pushaa kaikkea, yritän alkuviikosta selvitellä miten saan toimimaan.‼️‼️‼️
