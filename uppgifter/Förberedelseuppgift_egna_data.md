# Självstudier fre 21/8 & mån 24/8 (frivilligt): föreslå egen data & modell

**Bara relevant om ert team vill använda egen data och egen modell istället
för standarduppgiften** (prediktion av elpris, SE1–SE4, med
elprisetjustnu.se + SMHI-väderdata). Om ni är nöjda med standarduppgiften,
hoppa över detta — se istället det separata dokumentet om att bekanta sig
med den datan.

**Varför vi vill ha det skriftligt:** så att det faktiskt går att bedöma om
det är genomförbart innan teamen börjar jobba.

Fyll i varje avsnitt nedan. Korta svar räcker — det här är en
genomförbarhetskoll, inte en rapport. Om ett avsnitt inte är relevant,
skriv varför, lämna det inte tomt.

---

## 1. Problem & target

- En mening: vad ska ni predicera eller klassificera?
- Target-variabel — exakt definition, enhet och typ (regression /
  klassificering / annat).
- Hur ofta behöver en ny prediktion göras? (Varje timme? En gång om dagen?
  På begäran?)

## 2. Data — historisk

- Källa/källor, med länk.
- Vilket tidsspann finns tillgängligt, och ungefär hur mycket data (antal
  rader, storlek).
- Format och hur ni skulle hämta den (nedladdning, API, scraping).
- Krävs kostnad, registrering eller godkänd åtkomst? Redan bekräftat att
  det fungerar?

## 3. Data — levande / löpande

- Finns det en verkligt levande dataström som ger *ny* data, eller är det en fast historisk datamängd?
- Om levande: källa, uppdateringsfrekvens, åtkomstmetod, ev.
  nyckel/kostnad/rate limit.
- **När kommer facit?** När ni har gjort en prediktion, hur lång tid tar
  det innan ni vet om den stämde? 

## 4. Features (ungefärligt)

- Vilka indata går in i modellen, ungefär? Behöver inte vara en slutgiltig
  lista.
- Kommer alla från källorna ovan, eller finns det en dold extra källa?

## 5. Modell

- Ungefärlig typ/familj (regression, klassificering, tidsserie, något
  förtränat ni skulle finjustera, etc.) — behöver inte vara slutgiltigt.
- Några särskilda beräkningskrav (GPU för träning eller inferens)?

## 6. Passar det kursens verktyg?

- Är datan tabellformad, t exmed värden och tidsstämplar?
Om inte (bilder, fritext, etc.), hur tänker ni hantera det?

## 7. Deployment

- Öppna för allt som föreslås, eller vill ni specifikt ha GCP/Azure/något annat?
- Om något annat: har ni redan tillgång/krediter för det, eller kräver det
  ett nytt beslut från min sida?

## 8. Datastyrning (governance)

- Rör det här personlig, känslig eller på annat sätt skyddad data? En rad
  räcker — flagga det oavsett svar.
- Om datamängden skulle committas till ett publikt kursrepo, har ni rätt
  att vidaredistribuera den?

## 9. Team & reservplan

- Står hela teamet bakom det här, eller är det en persons förslag hittills?
- Om datakällan skulle falla bort halvvägs in, vad är reservplanen —
  byta till standarduppgiften, eller något annat?

## 10. Varför detta istället för standarduppgiften

- En eller två meningar. Vad gör det här värt den extra risken jämfört med
  ett projekt som redan är genomtestat från början till slut?

---

Lämna det här till mig (skriftligt) under nästa vecka!
