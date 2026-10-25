# Korpusbasierte lexikographische Arbeit: YouTube-Korpus zu Mental Health und Self-Improvement

**Forschungsbericht · Computational Linguistics 2025/2026 · MindWords Corpus Project**

Adelya Aibolova · Souhaila Derbal · Salah Eddine Nacer Benkhemis — Mai 2026

> Bereinigte Textfassung des eingereichten Berichts. Screenshots aus Sketch Engine, CQPweb und Google Colab sind hier nicht enthalten; die zugehörigen Befunde sind im Text beschrieben. Das Wörterbuch selbst ist unter https://adelyaaibolova.github.io/mindwords-corpus/ abrufbar (Daten: [`dictionary/entries.json`](../dictionary/entries.json)).

---

## 1. Forschungsziel, Forschungsfrage und Wörterbuchdesign

Das zentrale Ziel dieses Projekts ist die Erstellung eines spezialisierten englischsprachigen Korpus aus YouTube-Kommentarspalten im Bereich Mental Health und Self-Improvement sowie die Nutzung dieses Korpus als empirische Grundlage für ein korpusbasiertes Lernerwörterbuch. Das Wörterbuch trägt den Titel **MindWords – A Corpus-Based Dictionary of Mental Health Discourse on YouTube**.

### Forschungsfrage

> Welche lexikalischen Einheiten charakterisieren den Diskurs zu Mental Health und Self-Improvement auf YouTube, und wie werden diese in der authentischen digitalen Kommunikation eines Laienpublikums verwendet?

### Wörterbuchdesign

Das Wörterbuch richtet sich an zwei Zielgruppen: erstens junge Englischlernende und -sprechende (Alter 16–30), die im Social-Media-Kontext auf Mental-Health-Vokabular stoßen und dessen Bedeutung und Gebrauch verstehen möchten; zweitens Linguistinnen und Linguisten, die am Register digitaler Wellness-Diskurse interessiert sind.

Jeder Eintrag enthält:

- Stichwort mit grammatischer Kategorie und Frequenzindikator
- korpusbasierte Definition, die die tatsächliche Verwendung im YouTube-Diskurs widerspiegelt
- fünf authentische Korpusbeispiele aus der Sketch-Engine-Konkordanz
- *Common Group Words*: Kollokationsliste (korpusbelegt)
- mehrsprachige Übersetzungen: Arabisch, Deutsch, Französisch, Spanisch
- thematisch passender Zitatbeleg

Die Domäne Mental Health und Self-Improvement wurde ausgewählt, weil sie eine der am schnellsten wachsenden Content-Nischen auf YouTube darstellt. Der Diskurs verbindet klinische Psychologieterminologie (*anxiety, coping mechanism, burnout*), motivationales Vokabular (*mindset, growth, resilience*) sowie Neologismen und Lehnwörter aus der Social-Media-Kultur (*toxic positivity, shadow work, gaslighting*) mit authentischer Spontansprache in Kommentarspalten.

## 2. Korpusdesign

### 2.1 Korpustyp und Erhebung

Das Korpus ist ein spezialisiertes englischsprachiges Korpus aus YouTube-Kommentarspalten. Es umfasst nach der Bereinigung **623.452 Tokens** und bildet die analytische Grundlage aller Sketch-Engine-Abfragen.

Mithilfe der YouTube Data API v3 wurden Kommentare aus 14 ausgewählten YouTube-Videos erhoben. Die Videos repräsentieren eine breite Palette inhaltlicher Typen innerhalb der Domäne:

- **TEDx-Präsentationen:** Frederik Imbo, Jonathan Bricker
- **Podcast-Episode:** Jordan Peterson und Matt Rife
- **Mental-Health-Bildungskanäle:** Kati Morton, Dr. Paul Conti, Huberman Lab
- **Motivationsredner:** Dan Peña, Joe Dispenza
- **Social-Media-Influencer:** GrindBuddy, Thewizardliz, Ryan Robinson et Donked, Dry Creek Wrangler School

Insgesamt wurden 120.826 Rohkommentare aus 14 Quellen gesammelt:

| # | Video / Creator | Thema | Kommentare |
|---|---|---|---:|
| 1 | Frederik Imbo – How Not to Take Things Personally (TEDx) | Ego und emotionale Resilienz | 27.530 |
| 2 | Jordan Peterson und Matt Rife – Rife for Cancellation, EP 401 | Identität und sozialer Druck | 13.351 |
| 3 | Dan Peña – BEST Motivational Video Ever | Self-Improvement | 5.227 |
| 4 | GrindBuddy – If You Want to Be Wealthy and Happy | Self-Improvement | 6.777 |
| 5 | Joe Dispenza – This Will DELETE Your Old Self | Mental Health | 4.045 |
| 6 | Jordan Peterson – Fix Yourself Before It's Too Late | Mental Health | 2.250 |
| 7 | Dr. Paul Conti – How to Understand and Assess Your Mental Health | Mental Health | 4.044 |
| 8 | Jonathan Bricker – The Secret to Self Control (TEDxRainier) | Self-Improvement | 3.155 |
| 9 | Dry Creek Wrangler School – When You Just Haven't Quite Got It | Self-Improvement | 18.174 |
| 10 | Kati Morton – Are You a Narcissist? | Mental Health | 4.762 |
| 11 | Kati Morton – How to Overcome Childhood Emotional Neglect | Mental Health | 8.327 |
| 12 | Thewizardliz – Everything Will Be Fine | Self-Improvement | 3.668 |
| 13 | Kati Morton – The 6 Signs of High Functioning Depression | Mental Health | 12.873 |
| 14 | Ryan Robinson et Donked – It's Just There, Mate | Self-Improvement | 14.970 |
| | **Total, alle Videos** | | **120.826** |

Das Korpus wurde mithilfe eines Python-Skripts in Google Colab erstellt, das die YouTube Data API v3 abfragt. Kommentare und Antworten werden in einer CSV-Datei (`out.csv`) gespeichert, um sie zu bereinigen und in Sketch Engine bzw. CQPweb zu importieren. (Eine überarbeitete Version des Skripts liegt unter [`scripts/collect_comments.py`](../scripts/collect_comments.py).)

### 2.2 Problem der Korpusgröße und Reduktionsschritte

Als alle 120.826 Kommentare kombiniert und in Sketch Engine hochgeladen wurden, ergab sich ein Korpus von über 5 Millionen Tokens. Dieses Volumen war für eine effiziente Analyse im Projektzeitraum zu groß. Zwei Reduktionsschritte waren notwendig.

**Entscheidung 1 – Filterung nicht-englischer Kommentare.** Bei der Inspektion der Rohdaten zeigte sich, dass ein erheblicher Teil der Kommentare auf Arabisch verfasst war. Da das Projekt englischsprachige Diskurse untersucht, wurden diese Kommentare identifiziert und entfernt. Die Filterung wurde mit einem Python-Skript durchgeführt und produzierte die bereinigte Datei `combined_filtered.csv`. Nach der Filterung umfasst der Datensatz 79.646 Kommentare aus 14 Quelldateien mit den Spalten: `comment_id`, `type` (Topkommentar oder Antwort), Antwortanzahl, Like-Anzahl, Datum, Uhrzeit, Emojis, Kommentartext und Quelldatei.

*Hinweis:* Die Entdeckung nicht-englischer – insbesondere arabischer – Tokens war selbst ein lexikographisch bedeutsamer Befund und wird in Abschnitt 3.1 ausführlicher diskutiert.

**Entscheidung 2 – Auswahl von zwei Videos für Sketch Engine.** Auch nach der Sprachfilterung blieb der kombinierte Datensatz für eine vollständige Sketch-Engine-Analyse zu groß. Das Team entschied sich daher, die Kommentare von zwei YouTube-Videos für das endgültige Sketch-Engine-Korpus zu verwenden. Dieses reduzierte Korpus mit 623.452 Tokens wurde in Sketch Engine unter dem Korpusnamen *self improvement* hochgeladen und bildet die Grundlage aller nachfolgenden Analysen. Dadurch können einzelne Videos den Datensatz dominieren; diese Unbalanciertheit wird in Abschnitt 6 weiter diskutiert.

## 3. Angewandte Methoden der Datenextraktion

Die Analyse wurde in zwei parallelen Strängen durchgeführt: in Sketch Engine mit dem eigenen Korpus und in CQPweb mit POS-basierten Abfragen. Folgende Sketch-Engine-Funktionen wurden eingesetzt: Word Sketch, Word Sketch Difference, Thesaurus, Concordance, Wortliste und Keywords.

### 3.1 Keyword-Liste: Kandidatenauswahl und unerwarteter Befund

Der erste Analyseschritt war die Erstellung einer Keyword-Liste, die statistische Vergleiche zwischen dem eigenen Korpus und dem Referenzkorpus anstellt. Ausgewertet wurde Seite 2 der Liste (Rang 51–100).

**Bestätigte domänenspezifische Keywords:** *mindset* (Rang 81), *self-worth* (54), *overthinking* (60), *empathy* (69), *self-education* (78), *self-motivation* (93), *negativity* (94), *motivational* (64), *relatable* (77), *manifest* (87), *goosebumps* (90).

**Unerwarteter Befund:** In der Keyword-Liste erscheinen nicht-englische Tokens: das arabische Wort *Allah* (Rang 76) und ein weiteres arabisches Wort (Rang 100), außerdem *não* (Portugiesisch), *ik* (Niederländisch), *dank* (Niederländisch/Deutsch) und *que* (Spanisch/Französisch). Dieser Befund belegt, dass YouTube-Kommentarspalten genuin multilinguale Räume sind: Kommentatorinnen und Kommentatoren schreiben in ihrer Muttersprache, unabhängig von der Videosprache. Die arabischen Tokens legen nahe, dass arabischsprachige, vermutlich muslimische Jugendliche mit englischsprachigen Self-Improvement-Inhalten interagieren.

Die Keyword-Liste diente als Ausgangspunkt aller nachfolgenden gezielten Abfragen.

### 3.2 CQPweb – POS-basierte KWIC-Abfrage: *anxiety*

Die CQP-Abfrage `[pos="N.*"][word="anxiety"]` sucht nach allen Nomen, die unmittelbar vor dem Wort *anxiety* stehen. Sie lieferte 36 Treffer.

Die Abfrage bestätigte die Hypothese, dass *anxiety* im Korpus kaum allein steht, sondern häufig als Kopf einer Nominalkomposition fungiert. Identifizierte Komposita: *separation anxiety, trickle-down anxiety, job anxiety, shame anxiety, depression anxiety, death anxiety, functioning anxiety, level anxiety, attention anxiety*.

Besonders auffällig ist *trickle-down anxiety*: ein kreativer Neologismus, der einen Begriff aus dem Wirtschaftsdiskurs auf psychologischen Stress überträgt. Diese Abfrage war für den Wörterbucheintrag *anxiety* direkt verwertbar: Die Kompositastrukturen bilden die Grundlage der Kollokationsliste.

### 3.3 Sketch Engine – Word Sketch: *anxiety*

Der Word Sketch für *anxiety* (34 Instanzen als Nomen) zeigt grammatische Kollokatoren, gegliedert nach syntaktischer Relation:

| Syntaktische Relation | Wichtigste Kollokatoren | Korpusbeleg |
|---|---|---|
| Modifikatoren | social (häufigster), debilitating, constant, serious, unbearable | *my social anxiety* |
| Nomen modifiziert | disorder, introversion, self-hate, insomnia, depression, fear, attack | *anxiety disorder* |
| Verben (Objekt) | lessen, reduce, train, experience, understand, have | *lessen anxiety* |
| Koordination (and/or) | depression, introversion, self-hate, insomnia, stress, fear | *anxiety and depression* |
| Prädikativ (is a) | enemy (Gegennarrativ) | *Anxiety is not an enemy* |

**Zentraler Befund:** Die Prädikativkonstruktion liefert den Beleg *Anxiety is not an enemy*. Dies stellt ein lexikographisch bedeutsames Gegennarrativ dar: Angst wird nicht als zu bekämpfende Bedrohung, sondern als Signal gedeutet. Dieser Befund ist im Wörterbucheintrag als Gebrauchshinweis vermerkt.

### 3.4 Word Sketch Difference: *anxiety* vs. *healing*

Der Word-Sketch-Difference-Vergleich stellt die grammatischen Profile von *anxiety* (34 Instanzen) und *healing* (11 Instanzen) gegenüber:

| Relation | ANXIETY | HEALING |
|---|---|---|
| Modifikatoren | social, debilitating, constant, serious – vielfältig | spiritual – ausschließlich |
| Koordination (and/or) | depression, insomnia, self-hate, fear | business |
| Verben (als Objekt) | lessen, reduce, train, experience | need, be |
| Nomen modifiziert | disorder, insomnia, self-hate, fear, attack | art, medicine, herb, frequency |

*Anxiety* ist konkret, kategorisiert und klinisch gerahmt; *healing* ist abstrakt, spirituell und passiv. Beide Wörter gehören semantisch verschiedenen Subregistern an – ein zentraler lexikographischer Befund.

### 3.5 Konkordanz und Verteilung: *empathy*

Eine Konkordanzsuche nach *empathy* lieferte 94 Treffer (150,77 pro Million Tokens, 0,015 %). Sortiert nach GDEX (Good Dictionary Example Score) zeigt sich ein dominantes Muster:

- *Give yourself empathy and speak up* – erscheint in mehreren Varianten
- *Giving yourself empathy is helping yourself to love yourself more instead of taking yourself down*
- *I was not showing myself empathy for the smallest mistakes*

Im Standardenglisch ist *empathy* eine auf andere gerichtete Emotion. Im Korpus wird das Wort konsequent selbstgerichtet verwendet, als Synonym für Selbstmitgefühl oder Selbstvergebung. Dies stellt eine semantische Verschiebung dar, die im Wörterbucheintrag als Gebrauchshinweis explizit vermerkt ist.

### 3.6 Visual Word Sketch: *discipline*

**Einfache Variante (*discipline is a …*):** Die prädikative Konstruktion zeigt drei Nomen: *gateway*, *engine* und *freedom*. Alle drei sind Metaphern:

- *gateway*: Disziplin als instrumenteller Zugang zu etwas Besserem – Erfolg, Freiheit
- *engine*: Disziplin als treibende Kraft des Fortschritts – eine mechanische Metapher
- *freedom*: Paradoxon – Disziplin als Befreiung statt Einschränkung. Diese Formulierung ist aus dem Self-Improvement-Diskurs bekannt, u. a. popularisiert durch Jocko Willink.

**Vollständige Variante:**

- Modifikatoren: *little* und *small* (häufigste), *daily, conscious, sacrifice, growth*
- Nomen, die *discipline* modifiziert: *mindset, training, progress, culture, work, muscle* – besonders auffällig: *discipline muscle* als physische Metapher
- Koordination (and/or): *mindset, responsibility, self-motivation, sacrifice, progress, growth*
- Verben (als Objekt): *have, develop, be* – Disziplin gilt als erwerbbar

### 3.7 Visual Word Sketch: *self-education*

Der Visual Word Sketch zeigt folgende Relationen:

- Verben als Subjekt: *be, make, hit* – *self-education makes a difference*
- Verben als Objekt: *emphasize* (dominant) – präskriptives Register: Sprecher empfehlen Selbstbildung
- Nomen modifiziert: *self-discipline* (einziges) – autonomes Lernen und Verhaltenssteuerung gelten als untrennbar

Das Präfix *self-* erweist sich als morphologisch hochproduktiv: *self-education, self-discipline, self-worth, self-motivation, self-hate* – alle im Korpus vorhanden, alle verbunden mit dem Kernwertkonzept persönlicher Verantwortung.

### 3.8 Vergleich mit dem Referenzkorpus: *mindset* und *discipline*

**Mindset im Referenzkorpus.** Im Referenzkorpus English Web 2021 (enTenTen21) erscheint *mindset* in 500.885 Treffern (8,13 pro Million Tokens). Der Visual Word Sketch zeigt als häufigste Verben: *change, adopt, shift, cultivate, foster, embed, instill, empower, coach*; als Modifikatoren: *positive, entrepreneurial, growth, abundance, scarcity, analytical, patriarchal, colonial*. Im eigenen Korpus kollokiert *mindset* primär mit *discipline, training, progress* – ein persönlicheres, selbstbezogenes Register.

Der Thesaurus für *mindset* (499.315 Instanzen) identifiziert als nächste Synonyme: *attitude, mentality, thinking, confidence, lifestyle, habit, ambition, paradigm, worldview, creativity, ideology, ethic, ethos, aspiration, viewpoint*. Diese Synonymliste ermöglicht im Wörterbucheintrag die Abgrenzung von nahe verwandten Begriffen.

**Discipline im Referenzkorpus.** Im Referenzkorpus erscheint *discipline* mit 1.732.976 Instanzen. Modifikatoren: *academic, engineering, scientific, fiscal, strict, spiritual, church, STEM*. Verben: *instill, impose, enforce, exercise, maintain, practice, lack* – formal und hierarchisch. Im eigenen Korpus hingegen dominieren *discipline muscle, daily discipline, discipline is freedom* – ein völlig anderes, persönliches Ermächtigungsregister. Dieser Kontrast bestätigt den domänenspezifischen Charakter des eigenen Korpus eindrücklich.

## 4. Such-Historie

Der Suchprozess verlief in folgender Reihenfolge:

1. Keyword-Liste: Kandidatenidentifikation (*mindset, anxiety, empathy, discipline, overthinking, self-education, self-worth*)
2. *anxiety*: Word Sketch (Sketch Engine) und CQP-Abfrage `[pos="N.*"][word="anxiety"]`
3. *empathy*: Konkordanz GDEX-sortiert und Verteilungsanalyse
4. Word Sketch Difference: *anxiety* vs. *healing*
5. Visual Word Sketch: *discipline* (einfach und vollständig)
6. Visual Word Sketch: *self-education*
7. Vergleich mit Referenzkorpus: *mindset* und *discipline*
8. Thesaurus: *mindset* (Referenzkorpus)
9. Auswahl und Erstellung der Wörterbucheinträge

Kein Suchpfad führte in eine Sackgasse; alle Abfragen lieferten verwertbares Material. Die Keyword-Liste bildete den effektiven Ausgangspunkt für alle gezielten Folgeabfragen.

## 5. Ergebnis – Das Wörterbuch MindWords

Das Ergebnis der lexikographischen Arbeit ist das Wörterbuch *MindWords – A Corpus-Based Dictionary of Mental Health Discourse on YouTube*, das als interaktives HTML-Dokument vorliegt. Es enthält 11 Einträge in 5 thematischen Domänen mit Übersetzungen in 4 Sprachen.

| Domäne | Einträge |
|---|---|
| Emotional States | anxiety, overthinking |
| Self-Improvement | discipline, mindset, self-education |
| Support and Encouragement | empathy, you are not alone |
| Struggle and Recovery | healing, self-worth |
| Advice and Reflection | mindfulness, self-motivation |

### 5.1 Aufbau der Einträge und Definitionsquellen

Jeder Eintrag enthält: Stichwort mit Frequenzindikator und POS-Angabe, korpusbasierte Definition, fünf authentische Korpusbeispiele, *Common Group Words* (Kollokationsliste), eine mehrsprachige Übersetzungspalette sowie ein thematisches Zitat.

Definitionen wurden in allen Sprachen mit autoritativen Referenzwörterbüchern abgeglichen:

| Sprache | Referenzquelle |
|---|---|
| Englisch | Cambridge Dictionary – dictionary.cambridge.org |
| Deutsch | DWDS – Digitales Wörterbuch der deutschen Sprache (dwds.de) und Duden (duden.de) |
| Arabisch | Almaany – almaany.com |
| Französisch | Le Robert – dictionnaire.lerobert.com |
| Spanisch | RAE – Diccionario de la lengua española (dle.rae.es) |

### 5.2–5.4 Mustereinträge

Die Einträge, darunter die Mustereinträge *anxiety*, *discipline* und *mindset*, sind im Online-Wörterbuch einsehbar: https://adelyaaibolova.github.io/mindwords-corpus/. *Hinweis zur Repository-Fassung:* Bei der Vorbereitung des Repositorys wurden Korpusbeispiele und Kollokationen gegen das bereinigte Korpus geprüft und durch dort wörtlich belegte Beispiele ersetzt.

## 6. Bewertung des Ergebnisses

### 6.1 Abgleich mit den Wörterbuchzielen

Das Korpus und die Analysewerkzeuge haben gemeinsam ausreichend Material für vollständig ausgearbeitete Wörterbucheinträge geliefert; das ursprüngliche Designziel von 1–5 Einträgen wurde damit übertroffen. Die Korpusbeispiele sind authentisch, natürlich und kontextuell aussagekräftig; die GDEX-Sortierung in Sketch Engine war dabei besonders hilfreich. Das Wörterbuch erfüllt seine lexikographischen Funktionen: Es erklärt Fachvokabular für Lernende und dokumentiert domänenspezifische Verwendungsmuster für Forschende.

### 6.2 Werkzeugbewertung

**Sketch Engine** war das produktivste Werkzeug insgesamt:

- *Word Sketch*: vollständiges grammatisches Kollokationsprofil in einer Ansicht – direkt für Eintragskollokatoren verwertbar
- *Visual Word Sketch*: ermöglichte die Identifikation metaphorischer Konzeptualisierungen (*discipline* als gateway/engine/freedom)
- *GDEX-sortierte Konkordanz*: lieferte die besten Beispielsätze für die Einträge
- *Word Sketch Difference*: wertvoller Kontrast zwischen *anxiety* und *healing*
- *Keyword-Liste*: effizienter Ausgangspunkt für alle gezielten Abfragen
- *Thesaurus*: ermöglichte die Abgrenzung von Synonymen im Eintrag für *mindset*
- *Referenzkorpus-Vergleich*: schärfte das Verständnis des domänenspezifischen Registers

**CQPweb:** Am Ende haben wir CQP nicht oft benutzt, aber es war besonders nützlich für syntaxbasierte POS-Abfragen (z. B. `[pos="N.*"][word="anxiety"]`). Es ist mächtiger und flexibler als Sketch Engine für komplexe Abfragen, aber anspruchsvoller zu bedienen. Im Projekt hat es primär zu den Nominalkomposita für *anxiety* beigetragen.

### 6.3 Einschränkungen des Korpus

**Unbalanciertheit:** Die bedeutsamste Einschränkung ist die Unbalanciertheit. Die Entscheidung, nur zwei der vierzehn Videos zu verwenden, führt dazu, dass einzelne Videos die lexikalischen Muster dominieren. Dies ist besonders für *empathy* nachweisbar: Der Verteilungsgraph zeigt eindeutige Häufungsspitzen. Zukünftige Arbeiten sollten eine Balancierung anstreben.

**Arabische und nicht-englische Tokens:** Die Entdeckung arabischer Tokens in der Keyword-Liste zeigt ein Bereinigungsproblem: Ein Sprachfilter hätte bereits bei der Datenerhebung angewendet werden sollen. Gleiches gilt für YouTube-API-Metadaten-Artefakte (Zahlen und Zeitstempel in Kommentartexten), die in mehreren Konkordanzzeilen sichtbar sind.

**Fazit:** Trotz dieser Einschränkungen demonstriert das Projekt überzeugend, dass YouTube-Kommentarspalten eine produktive Korpusquelle für spezialisierte Lexikographie im Bereich zeitgenössischer digitaler Diskurse darstellen. Die Methodik – YouTube-API-basierte Erhebung, Sketch-Engine-Analyse, korpusgesteuerte Wörterbucherstellung – ist reproduzierbar und auf andere Domänen und Plattformen übertragbar.

## Literatur- und Quellenverzeichnis

**Wörterbücher**

- Cambridge Dictionary: https://dictionary.cambridge.org/
- DWDS – Digitales Wörterbuch der deutschen Sprache: https://www.dwds.de/
- Duden: https://www.duden.de/
- Almaany: https://www.almaany.com/
- Le Robert: https://dictionnaire.lerobert.com/
- RAE – Diccionario de la lengua española: https://dle.rae.es/

**Werkzeuge**

- Sketch Engine: https://app.sketchengine.eu/
- CQPweb – Corpus Query Processor
- YouTube Data API v3: https://developers.google.com/youtube
- Google Colab (Python): https://colab.research.google.com/
