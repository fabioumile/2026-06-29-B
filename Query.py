"""
le stesse tabelle che prendo per i nodi le prendo per gli archi e le duplico
#1:1 nel dataclass metti tipo oggetto, 1:N metti in un lato oggetto nell'altro lista di oggetti, N:M metti in entraambi i lati set di altri (In sql metti una terza tabella)
#query basi
        #SELECT colonne, (DISTINCT) elimina duplicati,  * all, COUNT(*) conta le righe o count(dist), AVG, MAX, MIN, SUM, AS peso crea nuova var, e1 e2 per coppie, coalesce(attributo,0) null->0
        #FROM  tabelle t1, t2
        #WHERE condizioni, e1.id < e2.id per evitare che coppia vada su se stesso,i.object = %s per query in db metto campo specifico,  <>  diverso  e elimina coppie < elimina anche permutazioni,
         AND OR, LIKE % sequenza qualsiasi, _ carattere qualsiasi, = 'valore riga'
        #tabella.nomecolonna = tabella2.nomecolonna condizione join, nel select metto t1.cod t2.cod, colonna = ( tabellaa annidata) o IN, NOT IN
        #GROUP BY attributi di raggruppamento "per ogni", tutto cio che ho nel select va qua
        # HAVING condizioni del raggr, è necessario il group by prima
        #ORDER BY colonne raggruppamento (ASC DESC) , tutto cio che ho nel select va qua
#nella query degli archi bisogna inserire le condizione dei query dei nodi

per le query arco:
select t1.order_id as o1, t2.order_id as o2, count(*) as peso
from (query nodo 1) as t1,
(query nodo 2) as t2
where t1.order_date <= t2.order_date and datediff(t1.order_date, t2.order_date) <= 5 and t1.order_id < t2.order_id
AND EXISTS (
    SELECT 1
    FROM tabella_di_giunzione AS J1, tabella_di_giunzione AS J2
    WHERE J1.foreign_key = A1.id    -- Collega la prima entità
      AND J2.foreign_key = A2.id    -- Collega la seconda entità
      AND J1.proprieta_comune = J2.proprieta_comune -- Il criterio di condivisione
)

1. Quando crei i NODI (getAllNodes)
Qui sì che ti serve SELECT a.*. Python deve costruire da zero l'oggetto @dataclass Album, quindi ha bisogno di AlbumId, Title e ArtistId. Se manca qualcosa, va in crash.
mettere anche group by ogni parametro
2. Quando crei gli ARCHI (getAllEdges)
Qui la situazione cambia completamente! Quando Python arriva a questo punto, i nodi esistono già in memoria e sono salvati dentro la tua idMap.


IDMB
#per sommare incassi:
SELECT SUM(CAST(REPLACE(worlwide_gross_income, '$ ', '') AS SIGNED)) AS totale_incassi
FROM movie
WHERE worlwide_gross_income IS NOT NULL

#num generi
SELECT m.title, COUNT(g.genre) AS num_generi
FROM movie m, genre g
WHERE m.id = g.movie_id
GROUP BY m.id, m.title

#Nodi=Registi con almeno un film di un certo genere
SELECT DISTINCT n.id, n.name
FROM names n, director_mapping dm, genre g
WHERE n.id = dm.name_id AND dm.movie_id = g.movie_id AND g.genre = %s

#Nodi = Film con rating medio > di una certa soglia
SELECT DISTINCT m.id, m.title
FROM movie m, ratings r
WHERE m.id = r.movie_id AND r.avg_rating > %s

#Nodi = Attori che hanno recitato in almeno N film
SELECT n.id, n.name
FROM names n, role_mapping rm
WHERE n.id = rm.name_id
GROUP BY n.id, n.name
HAVING COUNT(*) >= %s

#Nodi = film pubblicati in un intervallo di date, con median_rating minimo
SELECT DISTINCT m.id, m.title
FROM movie m, ratings r
WHERE m.id = r.movie_id
AND m.date_published BETWEEN %s AND %s
AND r.median_rating >= %s

#Nodi = registi che hanno diretto almeno un film di una production_company data
SELECT DISTINCT n.id, n.name
FROM names n, director_mapping dm, movie m
WHERE n.id = dm.name_id
AND dm.movie_id = m.id
AND m.production_company = %s

#Nodi = attori con height sopra soglia che hanno recitato in più di un genere
SELECT n.id, n.name
FROM names n, role_mapping rm, genre g
WHERE n.id = rm.name_id
AND rm.movie_id = g.movie_id
AND n.height > %s
GROUP BY n.id, n.name
HAVING COUNT(DISTINCT g.genre) > 1

#Nodi = generi con almeno N film aventi rating sopra soglia
SELECT g.genre
FROM genre g, ratings r
WHERE g.movie_id = r.movie_id
AND r.avg_rating > %s
GROUP BY g.genre
HAVING COUNT(DISTINCT g.movie_id) >= %s

#Nodi = paesi (movie.country) con almeno un film di un genere dato
SELECT DISTINCT m.country
FROM movie m, genre g
WHERE m.id = g.movie_id
AND g.genre = %s AND m.country IS NOT NULL

#Nodi = attori con data di nascita valida, che hanno recitato in film con incasso mondiale non
nullo
SELECT DISTINCT n.id, n.name
FROM names n, role_mapping rm, movie m
WHERE n.id = rm.name_id
AND rm.movie_id = m.id
AND n.date_of_birth IS NOT NULL
AND m.worlwide_gross_income IS NOT NULL

#Nodi = registi che hanno diretto film in almeno N generi diversi
SELECT n.id, n.name
FROM names n, director_mapping dm, genre g
WHERE n.id = dm.name_id
AND dm.movie_id = g.movie_id
GROUP BY n.id, n.name
HAVING COUNT(DISTINCT g.genre) >= %s

#Nodi = film con incasso mondiale sopra una soglia (gestione del formato $ ... )
SELECT m.id, m.title,
CAST(REPLACE(REPLACE(m.worlwide_gross_income, '$', ''), ',', '') AS UNSIGNED) AS incasso
FROM movie m
WHERE m.worlwide_gross_income IS NOT NULL
HAVING incasso > %s

#Nodi = attori il cui known_for_movies è valorizzato (per evitare errori di parsing in Python)
SELECT n.id, n.name, n.known_for_movies
FROM names n
WHERE n.known_for_movies IS NOT NULL

#2.NODI “ARRICCHITI” — classe con attributi extra
Pattern generale (come per la classe Artist con lista_brani e insieme_playlist ):
1. Query 1 → nodi base.
2. Query 2 (parametrica sull’id del nodo) → dato aggiuntivo 1, eseguita per ciascun nodo dentro un ciclo Python.
3. Query 3 (parametrica sull’id del nodo) → dato aggiuntivo 2, se serve.
4. Nel model si arricchisce l’oggetto con gli attributi extra prima di aggiungerlo al grafo.

2.1 Nodo = Attore, arricchito con “lista di tutti i film recitati” + “insieme dei generi recitati”
-- Query 1: nodi base (attori)
SELECT DISTINCT n.id, n.name
FROM names n, role_mapping rm
WHERE n.id = rm.name_id

-- Query 2: lista di tutti i film recitati da un dato attore (parametrica su name_id)
SELECT m.id, m.title
FROM movie m, role_mapping rm
WHERE m.id = rm.movie_id
AND rm.name_id = %s

-- Query 3: insieme dei generi in cui ha recitato un dato attore (parametrica su name_id)
SELECT DISTINCT g.genre
FROM genre g, role_mapping rm
WHERE g.movie_id = rm.movie_id
AND rm.name_id = %s

# Nel model, seguendo il pattern in due step:
def buildGraph(self):
    self._graph.clear()
    self._attori = DAO.getAllAttori()
    for a in self._attori:
        a.filmRecitati = DAO.getFilmRecitati(a.id) # lista di oggetti Film
        a.generiRecitati = set(DAO.getGeneriRecitati(a.id)) # insieme di stringhe
    self._graph.add_nodes_from(self._attori)

#2.2 Nodo = Regista, arricchito con “lista dei film diretti” + “dizionario anno → titoli”
-- Query 1: nodi base (registi)
SELECT DISTINCT n.id, n.name
FROM names n, director_mapping dm
WHERE n.id = dm.name_id

def buildGraph(self):
    self._graph.clear()
    self._registi = DAO.getAllRegisti()
    for reg in self._registi:
    righe = DAO.getFilmDiretti(reg.id)
        reg.filmDiretti = righe # lista completa
        reg.filmPerAnno = {}
        for riga in righe:
            reg.filmPerAnno.setdefault(riga["year"], []).append(riga["title"])
    self._graph.add_nodes_from(self._registi)

#2.3 Nodo = Film, arricchito con “lista di tutti gli interpreti” + “insieme dei generi”
#-- Query 1: nodi base (film con rating sopra soglia, es.)
SELECT DISTINCT m.id, m.title
FROM movie m, ratings r
WHERE m.id = r.movie_id
AND r.avg_rating > %s

#-- Query 2: tutti gli interpreti di un dato film (parametrica su movie_id)
SELECT n.id, n.name, rm.category
self._graph.add_nodes_from(self._attori)

#-- Query 2: tutti i film diretti da un dato regista, con anno (parametrica su name_id)
SELECT m.id, m.title, m.year
FROM movie m, director_mapping dm
WHERE m.id = dm.movie_id
AND dm.name_id = %s
ORDER BY m.year

FROM names n, role_mapping rm
WHERE n.id = rm.name_id
AND rm.movie_id = %s

-- Query 3: insieme dei generi di un dato film (parametrica su movie_id)
SELECT g.genre
FROM genre g
WHERE g.movie_id = %s

def buildGraph(self, soglia):
    self._graph.clear()
    self._film = DAO.getAllFilm(soglia)
    for f in self._film:
        f.interpreti = DAO.getInterpreti(f.id)
        f.generi = set(DAO.getGeneriFilm(f.id))
    self._graph.add_nodes_from(self._film)

#2.4 Variante “one-shot” con GROUP_CONCAT (se serve solo una stringa e non oggetti Python)
Se l’attributo extra deve essere solo una stringa concatenata (es. “elenco titoli separati da
virgola”) si può evitare il secondo giro di query e ottenere tutto in un’unica query SQL:
SELECT n.id, n.name,
GROUP_CONCAT(DISTINCT m.title SEPARATOR ', ') AS filmRecitati,
COUNT(DISTINCT g.genre) AS numGeneri
FROM names n, role_mapping rm, movie m, genre g
WHERE n.id = rm.name_id
AND rm.movie_id = m.id
AND g.movie_id = m.id
GROUP BY n.id, n.name

#Attenzione: GROUP_CONCAT va bene solo per attributi “stringa semplice” mostrati a video;
se servono oggetti Python distinti (per iterarci, ordinarli, ecc.) conviene sempre
l’approccio in due step (2.1–2.3).
#2.5 Nodo = Genere, arricchito con “numero totale di film” + “rating medio dei film di quel genere”
#-- Query 1: nodi base (generi)
SELECT DISTINCT g.genre FROM genre g

#-- Query 2: statistiche di un dato genere (parametrica su genre)
SELECT COUNT(DISTINCT g.movie_id) AS numFilm, AVG(r.avg_rating) AS ratingMedio
FROM genre g, ratings r
WHERE g.movie_id = r.movie_id
AND g.genre = %s

def buildGraph(self):
    self._graph.clear()
    self._generi = DAO.getAllGeneri()
    for gen in self._generi:
        numFilm, ratingMedio = DAO.getStatisticheGenere(gen.nome)
        gen.numFilm = numFilm
        gen.ratingMedio = ratingMedio
    self._graph.add_nodes_from(self._generi)

#ARCHI – connessioni tra nodi
#Arco tra registi se hanno co-diretto lo stesso film, peso = film in comune
SELECT DISTINCT n1.name AS registaA, n2.name AS registaB, COUNT(*) AS peso
FROM names n1, names n2, director_mapping dm1, director_mapping dm2
WHERE n1.id < n2.id AND dm1.name_id = n1.id AND dm2.name_id = n2.id
AND dm1.movie_id = dm2.movie_id
GROUP BY n1.id, n2.id

#Arco tra 2 attori se hanno recitato insieme, peso = numero film in comune
SELECT DISTINCT n1.name AS attoreA, n2.name AS attoreB, COUNT(*) AS peso
FROM names n1, names n2, role_mapping rm1, role_mapping rm2
WHERE n1.id < n2.id AND rm1.name_id = n1.id AND rm2.name_id = n2.id
AND rm1.movie_id = rm2.movie_id
GROUP BY n1.id, n2.id

#Arco tra film dello stesso genere, peso = somma avg_rating
SELECT DISTINCT m1.title AS filmA, m2.title AS filmB, (r1.avg_rating + r2.avg_rating) AS peso
FROM movie m1, movie m2, genre g1, genre g2, ratings r1, ratings r2
WHERE m1.id < m2.id AND g1.movie_id = m1.id AND g2.movie_id = m2.id
AND g1.genre = g2.genre AND r1.movie_id = m1.id AND r2.movie_id = m2.id
GROUP BY m1.id, m2.id

#Arco tra due generi se almeno un regista ha diretto film in entrambi, peso = numero di registi in comune
SELECT DISTINCT g1.genre AS genereA, g2.genre AS genereB, COUNT(DISTINCT dm1.name_id) AS peso
FROM genre g1, genre g2, director_mapping dm1, director_mapping dm2
WHERE g1.genre < g2.genre
AND dm1.movie_id = g1.movie_id
AND dm2.movie_id = g2.movie_id
AND dm1.name_id = dm2.name_id
GROUP BY g1.genre, g2.genre

#Arco tra film usciti entro 2 anni dello stesso genere, peso = (voti1+voti2) / |anno1-anno2|
SELECT DISTINCT m1.title AS filmA, m2.title AS filmB,(r1.total_votes + r2.total_votes) /ABS(m1.year - m2.year) AS peso
FROM movie m1, movie m2, genre g1, genre g2, ratings r1, ratings r2
WHERE m1.id < m2.id
AND g1.movie_id = m1.id AND g2.movie_id = m2.id
AND g1.genre = g2.genre AND r1.movie_id = m1.id AND r2.movie_id = m2.id
AND ABS(m1.year - m2.year) <= 2 AND ABS(m1.year - m2.year) != 0
GROUP BY m1.id, m2.id

#Arco tra due attori se hanno lavorato con lo stesso regista, peso = numero di registi in comune
SELECT DISTINCT rm1.name_id AS attoreA, rm2.name_id AS attoreB, COUNT(DISTINCT dm.name_id) AS peso
FROM role_mapping rm1, role_mapping rm2, director_mapping dm
WHERE rm1.name_id < rm2.name_id AND rm1.movie_id = dm.movie_id AND rm2.movie_id = dm.movie_id
GROUP BY rm1.name_id, rm2.name_id

#Arco NON pesato tra registi se hanno diretto un film della stessa production_company
SELECT DISTINCT dm1.name_id AS registaA, dm2.name_id AS registaB
FROM director_mapping dm1, director_mapping dm2, movie m1, movie m2
WHERE dm1.name_id < dm2.name_id AND dm1.movie_id = m1.id AND dm2.movie_id = m2.id
AND m1.production_company = m2.production_company AND m1.production_company IS NOT NULL
GROUP BY dm1.name_id, dm2.name_id

#Arco tra paesi se condividono un genere, peso = numero di film in comune per quel genere
SELECT DISTINCT m1.country AS paeseA, m2.country AS paeseB, COUNT(DISTINCT g1.movie_id) AS peso
FROM movie m1, movie m2, genre g1, genre g2
WHERE m1.country < m2.country
AND g1.movie_id = m1.id AND g2.movie_id = m2.id AND g1.genre = g2.genre
GROUP BY m1.country, m2.country

#Arco tra attori con età simile (entro K anni) che hanno recitato nello stesso genere, peso = film in comune
SELECT DISTINCT n1.id AS attoreA, n2.id AS attoreB,
COUNT(DISTINCT rm1.movie_id) AS peso
FROM names n1, names n2, role_mapping rm1, role_mapping rm2, genre g1, genre g2
WHERE n1.id < n2.id
AND n1.date_of_birth IS NOT NULL AND n2.date_of_birth IS NOT NULL
AND ABS(YEAR(n1.date_of_birth) - YEAR(n2.date_of_birth)) <= %s
AND rm1.name_id = n1.id AND rm2.name_id = n2.id
AND g1.movie_id = rm1.movie_id AND g2.movie_id = rm2.movie_id AND g1.genre = g2.genre
GROUP BY n1.id, n2.id

#Arco tra film con lo stesso regista ma generi diversi, peso = somma total_votes
SELECT DISTINCT m1.id AS filmA, m2.id AS filmB,
r1.total_votes + r2.total_votes AS peso
FROM movie m1, movie m2, director_mapping dm1, director_mapping dm2,
genre g1, genre g2, ratings r1, ratings r2
WHERE m1.id < m2.id
AND dm1.movie_id = m1.id AND dm2.movie_id = m2.id AND dm1.name_id = dm2.name_id
AND g1.movie_id = m1.id AND g2.movie_id = m2.id AND g1.genre <> g2.genre
AND r1.movie_id = m1.id AND r2.movie_id = m2.id
GROUP BY m1.id, m2.id

#Arco NON orientato e NON pesato tra due film se condividono lo stesso regista e la stessa production_company
SELECT DISTINCT m1.id AS filmA, m2.id AS filmB
FROM movie m1, movie m2, director_mapping dm1, director_mapping dm2
WHERE m1.id < m2.id
AND dm1.movie_id = m1.id AND dm2.movie_id = m2.id
AND dm1.name_id = dm2.name_id
AND m1.production_company = m2.production_company
AND m1.production_company IS NOT NULL
GROUP BY m1.id, m2.id

#4. ARCHI PESATI E ORIENTATI — approfondimento (molte casistiche)
Regola generale per il verso: si calcola un valore aggregato per ciascun nodo (in due
sottoquery p1 / p2 , o in Python), poi si confrontano i due valori con p1.valore >
p2.valore per decidere A → B . In caso di parità si può scegliere se scartare l’arco, o
inserirne uno per verso (a scelta del testo d’esame).

#Arco ORIENTATO: da A→B se A ha diretto più film di B (stesso genere)
#4.1 Registi — orientato per numero di film diretti in un genere (peso = somma film)
SELECT DISTINCT n1.name AS registaA, n2.name AS registaB,
p1.nFilm + p2.nFilm AS peso
FROM names n1, names n2,
director_mapping dm1, director_mapping dm2,
genre g1, genre g2,
(SELECT dm.name_id, COUNT(*) AS nFilm
FROM director_mapping dm, genre g
WHERE dm.movie_id = g.movie_id AND g.genre = %s
GROUP BY dm.name_id) p1,
(SELECT dm.name_id, COUNT(*) AS nFilm
FROM director_mapping dm, genre g
WHERE dm.movie_id = g.movie_id AND g.genre = %s
GROUP BY dm.name_id) p2
WHERE n1.id < n2.id
AND dm1.name_id = n1.id AND dm2.name_id = n2.id
AND g1.movie_id = dm1.movie_id AND g2.movie_id = dm2.movie_id
AND g1.genre = %s AND g2.genre = %s
AND p1.name_id = n1.id AND p2.name_id = n2.id
AND p1.nFilm > p2.nFilm
GROUP BY n1.id, n2.id

#4.2 Registi — orientato per numero TOTALE di film diretti (senza filtro genere), peso = differenza tra i due totali
SELECT DISTINCT n1.name AS registaA, n2.name AS registaB,
(p1.nFilm - p2.nFilm) AS peso
FROM names n1, names n2,
(SELECT dm.name_id, COUNT(*) AS nFilm
FROM director_mapping dm
GROUP BY dm.name_id) p1,
(SELECT dm.name_id, COUNT(*) AS nFilm
FROM director_mapping dm
GROUP BY dm.name_id) p2
WHERE n1.id <> n2.id
AND p1.name_id = n1.id AND p2.name_id = n2.id
AND p1.nFilm > p2.nFilm

#Arco ORIENTATO tra attori: da A→B se popolarità(A) > popolarità(B), peso=somma rating
#4.3 Attori — orientato per popolarità (somma rating dei film recitati), peso =  somma delle due popolarità
SELECT DISTINCT n1.name AS attoreA, n2.name AS attoreB, (p1.popolarita + p2.popolarita) AS peso
FROM names n1, names n2, role_mapping rm1, role_mapping rm2, (SELECT rm.name_id, SUM(r.avg_rating) AS popolarita
FROM role_mapping rm, ratings r WHERE rm.movie_id = r.movie_id GROUP BY rm.name_id) p1,
(SELECT rm.name_id, SUM(r.avg_rating) AS popolarita
FROM role_mapping rm, ratings r WHERE rm.movie_id = r.movie_id GROUP BY rm.name_id) p2
WHERE n1.id < n2.id AND rm1.name_id = n1.id AND rm2.name_id = n2.id
AND rm1.movie_id = rm2.movie_id AND p1.name_id = n1.id AND p2.name_id = n2.id
AND p1.popolarita > p2.popolarita GROUP BY n1.id, n2.id

#4.4 Film dello stesso genere — orientato in base alla data di uscita, peso = giorni di distanza
SELECT DISTINCT t1.movie_id AS filmA, t2.movie_id AS filmB,
DATEDIFF(t2.date_published, t1.date_published) AS peso
FROM (SELECT m.id AS movie_id, m.date_published
FROM movie m, genre g
WHERE m.id = g.movie_id AND g.genre = %s) t1,
(SELECT m.id AS movie_id, m.date_published
FROM movie m, genre g
WHERE m.id = g.movie_id AND g.genre = %s) t2
WHERE t1.movie_id <> t2.movie_id
AND t1.date_published < t2.date_published

#4.5 Film — orientato in base a un K massimo di giorni impostato dall’utente, peso normalizzato (voti / giorni)
SELECT DISTINCT t1.movie_id AS filmA, t2.movie_id AS filmB,
((t1.total_votes + t2.total_votes) / DATEDIFF(t2.date_published, t1.date_published)) AS peso
FROM (SELECT m.id AS movie_id, m.date_published, r.total_votes
FROM movie m, ratings r
WHERE m.id = r.movie_id) t1,
(SELECT m.id AS movie_id, m.date_published, r.total_votes
FROM movie m, ratings r
WHERE m.id = r.movie_id) t2
WHERE t1.movie_id <> t2.movie_id
AND t1.date_published < t2.date_published
AND DATEDIFF(t2.date_published, t1.date_published) <= %s
ORDER BY peso DESC


#4.6 Registi — orientato in base all’incasso mondiale totale dei propri film, peso = somma dei due incassi
SELECT DISTINCT n1.name AS registaA, n2.name AS registaB,
p1.incassoTot + p2.incassoTot AS peso
FROM names n1, names n2,
(SELECT dm.name_id,
SUM(CAST(REPLACE(REPLACE(m.worlwide_gross_income, '$', ''), ',', '') AS UNSIGNED)) AS incassoTot
FROM director_mapping dm, movie m
WHERE dm.movie_id = m.id AND m.worlwide_gross_income IS NOT NULL
GROUP BY dm.name_id) p1,
(SELECT dm.name_id,
SUM(CAST(REPLACE(REPLACE(m.worlwide_gross_income, '$', ''), ',', '') AS UNSIGNED)) AS incassoTot
FROM director_mapping dm, movie m
WHERE dm.movie_id = m.id AND m.worlwide_gross_income IS NOT NULL
GROUP BY dm.name_id) p2
WHERE n1.id <> n2.id
AND p1.name_id = n1.id AND p2.name_id = n2.id
AND p1.incassoTot > p2.incassoTot

#4.7 Attori — orientato in base all’altezza (height), peso = differenza di altezza
SELECT DISTINCT n1.id AS attoreA, n2.id AS attoreB,
(n1.height - n2.height) AS peso
FROM names n1, names n2
WHERE n1.id <> n2.id
AND n1.height IS NOT NULL AND n2.height IS NOT NULL
AND n1.height > n2.height

#4.8 Attori — orientato dal più anziano al più giovane (stesso genere recitato), peso = differenza di età in anni
SELECT DISTINCT n1.id AS attoreA, n2.id AS attoreB, (YEAR(n2.date_of_birth) - YEAR(n1.date_of_birth)) AS peso
FROM names n1, names n2, role_mapping rm1, role_mapping rm2, genre g1, genre g2
WHERE n1.id <> n2.id
AND n1.date_of_birth IS NOT NULL AND n2.date_of_birth IS NOT NULL
AND n1.date_of_birth < n2.date_of_birth
AND rm1.name_id = n1.id AND rm2.name_id = n2.id
AND g1.movie_id = rm1.movie_id AND g2.movie_id = rm2.movie_id
AND g1.genre = g2.genre
GROUP BY n1.id, n2.id

#4.9 Paesi — orientato per numero di film in un genere, peso = somma dei due totali
SELECT DISTINCT m1.country AS paeseA, m2.country AS paeseB,
p1.nFilm + p2.nFilm AS peso
FROM movie m1, movie m2, genre g1, genre g2,
(SELECT m.country, COUNT(*) AS nFilm
FROM movie m, genre g
WHERE m.id = g.movie_id AND g.genre = %s AND m.country IS NOT NULL
GROUP BY m.country) p1,
(SELECT m.country, COUNT(*) AS nFilm
FROM movie m, genre g
WHERE m.id = g.movie_id AND g.genre = %s AND m.country IS NOT NULL
GROUP BY m.country) p2
WHERE m1.country < m2.country
AND g1.movie_id = m1.id AND g2.movie_id = m2.id
AND g1.genre = %s AND g2.genre = %s
AND p1.country = m1.country AND p2.country = m2.country
AND p1.nFilm > p2.nFilm
GROUP BY m1.country, m2.country

#4.10 Generi — orientato per rating medio dei film del genere, peso = differenza tra le due medie
SELECT DISTINCT p1.genre AS genereA, p2.genre AS genereB, (p1.mediaRating - p2.mediaRating) AS peso
FROM (SELECT g.genre, AVG(r.avg_rating) AS mediaRating
FROM genre g, ratings r
WHERE g.movie_id = r.movie_id
GROUP BY g.genre) p1,
(SELECT g.genre, AVG(r.avg_rating) AS mediaRating
FROM genre g, ratings r
WHERE g.movie_id = r.movie_id
GROUP BY g.genre) p2
WHERE p1.genre <> p2.genre
AND p1.mediaRating > p2.mediaRating

#4.11 Registi — orientato per durata media dei propri film, peso = somma delle due durate medie
SELECT DISTINCT n1.name AS registaA, n2.name AS registaB, p1.durataMedia + p2.durataMedia AS peso
FROM names n1, names n2,
(SELECT dm.name_id, AVG(m.duration) AS durataMedia
FROM director_mapping dm, movie m
WHERE dm.movie_id = m.id AND m.duration IS NOT NULL
GROUP BY dm.name_id) p1,
(SELECT dm.name_id, AVG(m.duration) AS durataMedia
FROM director_mapping dm, movie m
WHERE dm.movie_id = m.id AND m.duration IS NOT NULL
GROUP BY dm.name_id) p2
WHERE n1.id <> n2.id
AND p1.name_id = n1.id AND p2.name_id = n2.id
AND p1.durataMedia > p2.durataMedia

#4.12 Production company — orientato per numero totale di voti ricevuti (total_votes) dai propri film, peso = somma
SELECT DISTINCT p1.production_company AS companyA, p2.production_company AS companyB, p1.votiTot + p2.votiTot AS peso
FROM (SELECT m.production_company, SUM(r.total_votes) AS votiTot
FROM movie m, ratings r
WHERE m.id = r.movie_id AND m.production_company IS NOT NULL
GROUP BY m.production_company) p1,
(SELECT m.production_company, SUM(r.total_votes) AS votiTot
FROM movie m, ratings r
WHERE m.id = r.movie_id AND m.production_company IS NOT NULL
GROUP BY m.production_company) p2
WHERE p1.production_company <> p2.production_company
AND p1.votiTot > p2.votiTot

#4.13 Attori — orientato per numero di generi distinti recitati, peso = somma dei due conteggi (query interamente SQL, senza sottoquery separate)
SELECT DISTINCT rm1.name_id AS attoreA, rm2.name_id AS attoreB,
COUNT(DISTINCT g1.genre) + COUNT(DISTINCT g2.genre) AS peso
FROM role_mapping rm1, role_mapping rm2, genre g1, genre g2
WHERE rm1.name_id <> rm2.name_id
AND g1.movie_id = rm1.movie_id
AND g2.movie_id = rm2.movie_id
GROUP BY rm1.name_id, rm2.name_id
HAVING COUNT(DISTINCT g1.genre) > COUNT(DISTINCT g2.genre)

SELECT DISTINCT p1.production_company AS companyA, p2.production_company AS companyB,
p1.votiTot + p2.votiTot AS peso
FROM (SELECT m.production_company, SUM(r.total_votes) AS votiTot
FROM movie m, ratings r
WHERE m.id = r.movie_id AND m.production_company IS NOT NULL
GROUP BY m.production_company) p1,
(SELECT m.production_company, SUM(r.total_votes) AS votiTot
FROM movie m, ratings r
WHERE m.id = r.movie_id AND m.production_company IS NOT NULL
GROUP BY m.production_company) p2
WHERE p1.production_company <> p2.production_company
AND p1.votiTot > p2.votiTot


#4.14 Film — orientato dal film con median_rating più basso a quello più alto (stesso regista), peso = differenza tra i due median_rating
SELECT DISTINCT m1.id AS filmA, m2.id AS filmB, (r2.median_rating - r1.median_rating) AS peso
FROM movie m1, movie m2, director_mapping dm1, director_mapping dm2, ratings r1, ratings r2
WHERE m1.id <> m2.id
AND dm1.movie_id = m1.id AND dm2.movie_id = m2.id
AND dm1.name_id = dm2.name_id
AND r1.movie_id = m1.id AND r2.movie_id = m2.id
AND r1.median_rating < r2.median_rating

#4.15 Registi — orientato per verso “cronologico” in base al primo film diretto, peso = anni di distanza tra i due esordi
SELECT DISTINCT p1.name_id AS registaA, p2.name_id AS registaB, (p2.primoAnno - p1.primoAnno) AS peso
FROM (SELECT dm.name_id, MIN(m.year) AS primoAnno
FROM director_mapping dm, movie m
WHERE dm.movie_id = m.id
GROUP BY dm.name_id) p1,
(SELECT dm.name_id, MIN(m.year) AS primoAnno
FROM director_mapping dm, movie m
WHERE dm.movie_id = m.id
GROUP BY dm.name_id) p2
WHERE p1.name_id <> p2.name_id
AND p1.primoAnno < p2.primoAnno

select t1.id as n1, t2.id as n2, t1.fatturato as fatt1, t2.fatturato as fatt2, (t1.fatturato+t2.fatturato) as peso
from (select n.*, SUM(CAST(REPLACE(m.worlwide_gross_income, '$ ', '') AS SIGNED)) AS fatturato
from names n,role_mapping rm, ratings r, movie m
where n.id = rm.name_id and rm.movie_id = m.id and m.id=r.movie_id and r.avg_rating >= 1.0 and r.avg_rating <= 3.0 and m.worlwide_gross_income IS NOT NULL
and n.date_of_birth is not null
group by n.id) as t1,
(select n.*, SUM(CAST(REPLACE(m.worlwide_gross_income, '$ ', '') AS SIGNED)) AS fatturato
from names n,role_mapping rm, ratings r, movie m
where n.id = rm.name_id and rm.movie_id = m.id and m.id=r.movie_id and r.avg_rating >= 1.0 and r.avg_rating <= 3.0 and m.worlwide_gross_income IS NOT NULL
and n.date_of_birth is not null
group by n.id) as t2
where t1.id < t2.id
AND EXISTS (
    SELECT *
    FROM role_mapping rm1, role_mapping rm2
    WHERE rm1.name_id = t1.id #se attore1 ha recitato nello stesso film
      AND rm2.name_id = t2.id # se "" 2 ""
      AND rm1.movie_id = rm2.movie_id  #join
)
order by peso desc

#QUERY AVANZATE IMDB
#Registi con numero di generi distinti diretti superiore alla media
SELECT n.name, sub.numGeneri
FROM names n,
(SELECT dm.name_id, COUNT(DISTINCT g.genre) AS numGeneri
FROM director_mapping dm, genre g
WHERE dm.movie_id = g.movie_id
GROUP BY dm.name_id) sub
WHERE n.id = sub.name_id
AND sub.numGeneri > (
SELECT AVG(cnt.numGeneri)
FROM (SELECT dm2.name_id, COUNT(DISTINCT g2.genre) AS numGeneri
FROM director_mapping dm2, genre g2
WHERE dm2.movie_id = g2.movie_id
GROUP BY dm2.name_id) cnt
)
ORDER BY sub.numGeneri DESC

#Attori che hanno recitato in TUTTI i film di un dato regista
SELECT n.name
FROM names n
WHERE NOT EXISTS (
SELECT dm.movie_id FROM director_mapping dm
WHERE dm.name_id = %s
AND NOT EXISTS (
SELECT * FROM role_mapping rm
WHERE rm.name_id = n.id
AND rm.movie_id = dm.movie_id
    )
)

#Registi che hanno diretto film in TUTTI i generi selezionati (divisione relazionale)
SELECT n.name FROM names n
WHERE NOT EXISTS (
SELECT g.genre FROM genre g WHERE g.genre IN ('Drama', 'Comedy', 'Thriller')
AND NOT EXISTS (
SELECT * FROM director_mapping dm, genre g2
WHERE dm.name_id = n.id AND dm.movie_id = g2.movie_id AND g2.genre = g.genre
    )
)

#Film con più generi della media
SELECT m.title, COUNT(g.genre) AS num_generi
FROM movie m, genre g WHERE m.id = g.movie_id GROUP BY m.id, m.title
HAVING COUNT(g.genre) > (SELECT AVG(cnt) FROM
(SELECT movie_id, COUNT(*) AS cnt FROM genre GROUP BY movie_id) sub)

#Top N registi per numero film in un genere, con media rating
SELECT n.name, COUNT(DISTINCT dm.movie_id) AS num_film, AVG(r.avg_rating) AS media
FROM names n, director_mapping dm, genre g, ratings r
WHERE n.id = dm.name_id AND dm.movie_id = g.movie_id AND g.genre = %s AND r.movie_id = dm.movie_id
GROUP BY n.id, n.name ORDER BY num_film DESC, media DESC LIMIT %s

#Top N attori per numero di film con rating sopra soglia
SELECT n.name, COUNT(DISTINCT rm.movie_id) AS numFilm
FROM names n, role_mapping rm, ratings r
WHERE n.id = rm.name_id
AND rm.movie_id = r.movie_id
AND r.avg_rating > %s
GROUP BY n.id, n.name
ORDER BY numFilm DESC
LIMIT %s

#Attori con popolarità (somma rating dei film recitati) superiore alla media
SELECT n.name, sub.popolarita
FROM names n,
(SELECT rm.name_id, SUM(r.avg_rating) AS popolarita
FROM role_mapping rm, ratings r
WHERE rm.movie_id = r.movie_id
GROUP BY rm.name_id) sub
WHERE n.id = sub.name_id
AND sub.popolarita > (
SELECT AVG(pop.popolarita)
FROM (SELECT rm2.name_id, SUM(r2.avg_rating) AS popolarita
FROM role_mapping rm2, ratings r2
WHERE rm2.movie_id = r2.movie_id
GROUP BY rm2.name_id) pop
)
ORDER BY sub.popolarita DESC
"""