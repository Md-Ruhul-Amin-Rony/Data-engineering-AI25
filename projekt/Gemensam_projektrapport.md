# Gemensam projektrapport

Lämnas in **en gång per grupp** senast **måndag 5/10 2026 kl. 23:59**.
Skicka rapporten till mig i Teams eller via e-post.

Rapporten beskriver er gemensamma lösning och hur ni har arbetat. Den ska
stämma överens med kod, GitHub-tavla, pull requests och det ni visar i
slutredovisningen.

Den är inte samma sak som den **individuella analysen av tekniskt bidrag**.
Den individuella analysen skrivs och lämnas in av varje student för sig senast
**fredag 9/10 2026 kl. 23:59**.

## Innehåll

Använd rubrikerna nedan. Skriv konkret om ert eget projekt, inte generellt om
teknik.

### 1. Systemet

Beskriv systemet kort:

- datakällor
- hur data rör sig genom `raw__`, `stg__` och `feat__`
- träning och modell i Hugging Face Hub
- inferenstjänst och driftsättning

En enkel skiss över flödet får gärna ingå.

### 2. Viktiga tekniska val

Beskriv 2–4 val som har påverkat ert projekt. De behöver inte vara stora eller
helt fria val. Det kan också vara ett val att följa en given exempelkod, justera
den när den inte passar eller välja en konkret lösning utifrån era data och
förutsättningar.

För varje val: vad var utgångspunkten, vad gjorde ni och varför? Nämn
alternativ bara om ni faktiskt övervägde dem.

Det kan till exempel handla om datamodell, validering, feature-logik,
träningsintervall, modellversion eller hur tjänsten hämtar sina features. Det
kan också handla om en ändring eller avgränsning som ni gjorde medan ni
arbetade med exempelkod.

### 3. Drift och spårbarhet

Förklara hur systemet körs och hur ni kan följa en prediktion i efterhand:

- schemalagda jobb och eventuella manuella triggers
- CI, tester och linting
- hur kod granskas och går till `main`
- vilken data, kodversion, modellversion och tidpunkt som hör till en
  prediktion

Beskriv också vad som fortfarande är manuellt eller ofärdigt, om något sådant
finns.

### 4. Monitorering och datakvalitet

Beskriv hur ni jämför prediktioner med utfall när facit finns, vilket felmått
ni använder och hur resultatet visas.

Ta också upp minst en datakvalitetskontroll: vad kontrolleras, vad händer vid
fel och vem behöver agera?

### 5. Etik och data governance

Sammanfatta er bedömning av:

- datakällor, villkor och attribution
- personuppgifter eller annan känslig information i data och loggar
- ansvar för åtkomst, lagring och radering efter kursen

Hänvisa till `docs/etik.md` om ni har en mer detaljerad text där.

### 6. Teknisk reflektion

Koppla projektet till kursens teori:

- hur Docker och Kubernetes fungerar, och varför Kubernetes passar eller inte
  passar er lösning
- vilka molntjänster ni använder och hur en motsvarande lösning hade kunnat
  se ut i AWS, Azure och Google Cloud
- hur Spark och Databricks hade kunnat vara relevanta vid större datamängder,
  och varför ert nuvarande upplägg räcker eller inte räcker

### 7. Retrospektiv

Beskriv kort hur ni arbetade tillsammans:

- något som fungerade
- något som inte fungerade
- en förändring ni gjorde under projektet och vad den ledde till
- vad ni skulle ändra nästa gång

Använd konkreta exempel från er tavla, era pull requests eller era
retrospektiv.

## Innan ni lämnar in

- Kontrollera att alla delar ovan finns med.
- Kontrollera att påståenden går att känna igen i ert repo och i ert system.
- Kontrollera att alla i gruppen har läst rapporten.
