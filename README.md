# Koiratietokanta

Tietokannat & web-ohjelmoinnit 2025 kurssi.


🐾 Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.


🐾 Käyttäjä pystyy lisäämään sovellukseen koiran, antamaan sille nimen, rodun ja iän. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään tietoja.


🐾 Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät koirat.


🐾 Käyttäjä pystyy etsimään tietoa koirista hakusanoilla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä ilmoituksia.


🐾 Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja kuten kuinka monta koiraa omistaa ja niiden tiedot sekä kuinka monta kertaa on jättänyt ilmoituksen.


🐾 Käyttäjä pystyy valitsemaan koirallensa yhden tai useamman luokan, kuten onko koira minkä kokoinen tai millainen sen luonne on. Mahdolliset luokat ovat tietokannassa.


🐾 Sovelluksessa on pääasiallisen tietokohteen lisäksi toissijainen tietokohde, jossa pystyy kertomaan enemmän koirastaan, esim. etsii seuraa agilityyn, lenkeille, kisoihin, koirapuistoon, tarvitsee välillä ulkoiluttajaa.

Miten sovellusta voi käyttää?
- Kopioi projektin linkki painamalla vihreätä Code-nappia > SSH > ota linkki talteen Clonesta 
```bash
(git@github.com:emmapiittala/koiratietokanta.git)
```

- Avaa komentorivi ja kloonaa projekti komennolla: git clone sekä perään linkki. 
```git clone git@github.com:emmapiittala/koiratietokanta.git```
Näin sinulle pitäisi asentua koiratietokanta-projektini. 

- Mene koiratietokanta projektiin ja aktivoi virtuaaliympäristö komennolla: ```source venv/bin/activate```

- asenna pythoniin kirjasto: pip install flask

- Sovelluksen saa käynnistymään kirjoittamalla komentoriville: flask run ja kopioimalla komentoriville tulevan selaimen linkin (http://127.0.0.1:5000)

- Liitettyä linkin selaimeen, pääset koiratietokannan nettisivuille. Tässä versiossa pystyt luomaan tunnuksen, kirjautumaan sisään, etsimään ilmoituksia sekä vain kirjautuneet käyttäjät pystyvät myös luomaan ilmoituksia. 