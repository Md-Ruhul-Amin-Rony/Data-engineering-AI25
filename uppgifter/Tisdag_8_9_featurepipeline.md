# Tisdag 8/9: Feature-pipeline

## Dagens mål

Vi separerar feature-beräkningen från modellträningen.

```text
stg__ → feature-pipeline → feat__daily → train.py → modell
```

`feat__daily` byggs av feature-pipelinen. `train.py` ska senare läsa från tabellen, men ska inte skriva till den.

## Börja här

Använd `feature_pipeline_starter.py` som utgångspunkt. Kopiera den till projektets rot och döp den till `feature_pipeline.py`.

1. Bestäm vad en rad i `feat__daily` betyder för er target.
2. Skapa tabellen med en egen .sql-fil och committa den.
3. Återanvänd feature-logiken från `train.py` så att den kan läsa från era `stg__`-vyer.
4. Kör feature-steget lokalt. Den här första versionen läser hela den historik som finns i era `stg__`-vyer.
5. Kontrollera resultatet i databasen:

```sql
SELECT count(*), min(target_date), max(target_date)
FROM feat__daily;
```

## Dagens checkpoint

Innan ni börjar med träning ska ni kunna visa:

- tabellen `feat__daily`
- hur många rader den innehåller
- er senaste commit

Om ni kör fast: visa felmeddelandet, vad ni försökte göra och vilken del av flödet som inte fungerar.

## Målbild vecka 5

| När | Minimiläge | Idealisk målbild |
|---|---|---|
| Tisdag 8/9 | Ni kan förklara flödet till `feat__daily`, har bestämt tabellens form och kan visa nästa steg eller en konkret blockerare. | `feat__daily` är designad, .sql-filen är committad och en första lokal feature-körning är påbörjad. |
| Onsdag 9/9 | Feature-steget kan köras lokalt och skriver minst en rad till `feat__daily`. | Historisk feature-körning är gjord. Tabellen har tillräckligt många rader för träning och en andra körning skapar inte dubbletter. |
| Torsdag 10/9 | Ni har ett Hugging Face-repo och har registrerat eller är redo att registrera den CSV-tränade basmodellen med mått. | `train.py` läser features från Postgres och en första modellversion med mått finns i Hugging Face. |
| Fredag 11/9 | Sprint 1-tavlan visar verkligt läge och ni har haft en retrospektiv. | Ingestion och feature-pipeline fungerar för det överenskomna flödet, första modellversionen är spårbar och Sprint 2 är realistiskt planerad. |

Om ni inte hinner byta `train.py` till Postgres före torsdag gör ni ändå Hugging Face-övningen med den CSV-tränade basmodellen. Visa sedan ärligt vad som återstår.

## För grupper med egen data

Följ era godkända projektspecifika mål. Ni behöver inte använda standarduppgiftens tabellnamn eller steg-för-steg-upplägg, men er motsvarighet till feature-tabellen ska vara tydlig och träningsbar. Minimiläge och idealisk målbild ska motsvara samma arkitektoniska steg som i tabellen ovan.

Eftersom ni använder egen data ska ni senast fredag 11/9 lägga en kort notering om data governance i repot: var datan kommer från, om den innehåller personuppgifter eller har användningsvillkor, och var den lagras.
