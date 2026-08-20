# Självstudier fre 21/8 & mån 24/8: bekanta dig med projektdatan

För er som kör standarduppgiften — prediktion av svenskt elpris med väder
som feature. (Om ni istället föreslår egen data, använd det andra
dokumentet, inte det här.)

Ingen git, inget repo, ingen Docker den här gången — bara peta på två
gratis API:er utan nyckel i en scratch-mapp i din Codespace, precis som du
gjorde med SMHI i vecka 1. Inget att installera, inget att committa.

**Varför nu, innan team och elområden är tilldelade:** ni får ert
specifika elområde och target på måndag i kickoff-workshoppen. Det här
handlar om att bli bekväm med *formen* på datan innan dess, så att
diskussionen på workshoppen kan handla om ert faktiska elområde istället
för om hur API:et fungerar.

## Uppgift 

### 1. Hämta några priser

Pris-API:et kräver ingen nyckel:
`https://www.elprisetjustnu.se/api/v1/prices/<ÅR>/<MM>-<DD>_<OMRÅDE>.json`,
där `<OMRÅDE>` är `SE1`, `SE2`, `SE3` eller `SE4`. Välj vilket område som
helst — ni är inte bundna till det, det här är bara utforskning.

Hämta några olika dagar: en från förra veckan, en från sex månader sedan,
och en från **före 1 oktober 2025**. Titta på den råa JSON-datan. Hur
många prispunkter finns i en enskild dags fil? Ändras det talet någonstans
i ert datumintervall?

### 2. Hämta lite väder

Ni kan få fram temperaturprognoser från SMHI:s API med ett anrop som t ex
curl "https://opendata-download-metfcst.smhi.se/api/category/snow1g/version/1/geotype/point/lon/18.0549/lat/59.3417/data.json?parameters=air_temperature"
Välj en station i närheten av det ni gissar spelar roll för ert elområde, och hämta
temperatur (eller en annan parameter) för samma datumintervall som ovan.
Ni kan hitta stationskoderna här: https://www.smhi.se/data/hitta-data-for-en-plats/ladda-ner-vaderobservationer/airtemperatureInstant

Man kan också få fram historiska data i en CSV-fil med:
curl "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/1/station/98230/period/corrected-archive/data.csv"

### 3. Lägg dem bredvid varandra

Behöver inte vara en riktig analys — en snabb graf eller bara att titta på
två kolumner bredvid varandra räcker. För en vinterdag och en sommardag:
rör sig prisserien på något synligt relaterat sätt till temperaturen? Ni
behöver ingen slutsats, bara ett första intryck.

### 4. Hitta informationsgränsen

Morgondagens priser publiceras av källan runt kl. 13:00 dagen innan, inte
vid midnatt. Testa att hämta morgondagens fil både före och efter den
tiden (eller kolla helt enkelt vad API:et svarar för ett datum som ännu
inte publicerats).

Skriv en mening: varför spelar det här roll för en modell som ska göra en
verklig prediktion, till skillnad från en som bara utvärderas mot data som
redan finns fullt tillgänglig? 

## Ta med till tisdagen

Inget skriftligt att lämna in — men kom med en konkret observation från
steg 1–4 (hur data ser ut, något som
förvånade dig med något av API:erna, etc). Team och elområde bestämmer vi senare.
