# Onsdag 9/9: få feature-pipelinen att fungera

Online handledning 09:00–12:00.

Kom med ett konkret problem, en länk till er pull request eller senaste commit, och det felmeddelande eller resultat ni ser.

## Prioritet i rätt ordning

### 1. Få skriptet att köra lokalt

Feature-steget ska läsa från `stg__` och skriva till `feat__daily`.

Här kontrollerar ni att anslutningen, läsningen från `stg__`, feature-beräkningen och upserten fungerar. Lägg inte tid på träning, Hugging Face eller schemaläggning ännu.

### 2. Kontrollera att hela historiken kom med

Den nuvarande lösningen läser hela historiken från `stg__` vid varje körning. När skriptet fungerar ska ni därför kontrollera att `feat__daily` verkligen täcker den historik ni förväntar er:

Kontrollera tabellen:

```sql
SELECT count(*), min(target_date), max(target_date)
FROM feat__daily;
```

Ni behöver tillräckligt många rader för att kunna träna en modell i morgon.

`target_date` är dagen som ska förutsägas. Högsta datumet kan därför vara en dag efter den senaste prisdagen. Den sista raden saknar normalt `y` och används inte vid träning.

### 3. Kör samma sak en gång till

`feat__daily` ska inte få fler rader av en andra identisk körning. Om antalet ökar har ni sannolikt inte en korrekt upsert.

Kontrollera också att tabellen saknar dubbletter:

```sql
SELECT price_area, target_date, COUNT(*)
FROM feat__daily
GROUP BY price_area, target_date
HAVING COUNT(*) > 1;
```

Frågan ska ge **0 rader**.

### 4. Schemalägg först när det fungerar

När feature-steget fungerar manuellt kan ni koppla det till er befintliga GitHub Actions-workflow. Bygg inte en ny workflow från början.

## Mål för dagen

**Minimiläge:** feature-steget körs lokalt utan fel och skriver feature-rader till `feat__daily`.

**Idealisk målbild:** hela historiken är byggd, tabellen har tillräckligt många rader för träning och en andra körning skapar inte dubbletter.

Commit:a och pusha ändringarna, eller öppna en pull request, innan dagen är slut.

## Inför torsdag

Ha tillgång till en e-postadress ni kan öppna under lektionen. På torsdag arbetar vi med Hugging Face och modellregister.

Om feature-pipelinen inte är klar kan ni ändå registrera en modell tränad från CSV-filerna. Visa då tydligt vad som återstår.
