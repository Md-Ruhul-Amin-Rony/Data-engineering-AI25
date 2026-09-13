# Etikövning tisdag 15/9, c:a 11:30–12:00

Fyll i detta i grupp. Det är förberedelser för
etikdelen av gruppredovisningen på torsdag.

När man formulerar en etisk fråga eller problem kan det
vara användbart att tänka på tre saker: 

- Blir någon **person** drabbad?
- Vad blir **konsekvensen**?
- Vad är **mekanismen** dvs vad är det som gör att personen drabbas. 

Kopiera denna fil till ert repo som `docs/etik.md` och skriv svaren där.

---

## Fråga 1 — Vilka data har ni idag, kommer nya data att tillkomma, och rör data specifika personer?

Starta med systemet ni har idag:

- [ ] Träningsdata: vad finns där, och är något av det om specifika personer?
- [ ] Databas: vad lagras i Neon, vem är ansvarig för det, och när kommer det att raderas efter kursen?
- [ ] Ert eget repo och secrets: är något personligt committat någonstans?
- [ ] Framtida API: när ni publicerar prediktionstjänsten, vad kommer ni att logga om varje anrop? Vem behöver tillgång till den informationen och hur länge kommer den att sparas?
      

## Fråga 2 — Vad får ni göra med de data ni hämtat?

För standardprojektet använder ni nedanstående källor (de andra projekten har sina egna):

> - **[SMHI Open Data](https://www.smhi.se/data/om-smhis-data/villkor-for-anvandning):**
>   CC BY 4.0. Ange SMHI som källa och beskriv er bearbetning av datan.
> - **[elprisetjustnu.se](https://www.elprisetjustnu.se/elpris-api)**: API:t beskrivs som öppet och fritt utan formell licens. Dokumentera kort vad som står där nu och när ni läste det.

För varje datakälla, skriv ner:

- Källa 
- Licens 
- Behöver ni hänvisa till källan? 
- Får ni återpublicera råa data? 
- Var och när ni läste villkoren 

Lyder er nuvarande lösning villkoren? 

Kolla också vad som gäller för eventuella villkor eller begränsningar för API-användning. När ni anropar API:er använder ni någon annans infrastruktur och ibland har de regler kring detta.

---

## Fråga 3 — Vem blir påverkad av era prediktioner?

Beskriv en specifik person och hur den kan påverkas.

- Vem tjänar på att en prognos är korrekt? Vad kan de göra som andra inte kan?
- Vem kan inte agera på prediktionen alls och varför?
- Är ett fel på t ex 30% ett lika stort problem för båda grupperna?
- Kommer ert system att lägga mer eller mindre ansvar på specifika grupper?
- Hur stort ansvar har ni att berätta om modellens begränsningar? Är det etiskt att be folk använda en modell som har negativt R^2-värde?

---

## Fråga 4 — Förändras något om systemet skalas upp, säljs, eller automatiseras?

Välj en av dessa tre förändringar (uppskalning, försäljning, automatisering).

**Om systemet såldes.** Vad skulle en betalande kund kräva eller ha rätt till som den inte har nu? T ex garantier om accuracy, tillgänglighet, information om när systemet ligger nere, osv? Vad händer om prediktionerna har helt fel?

**Om systemet skalades upp rejält** Era prediktioner skulle, om de följdes av hundratusentals hushåll, ändra elkonsumtionen vilket skulle kunna ha effekter på priset. Vad händer då med prediktionerna? 

**Om lösningen automatiserades.** En siffra på en webbsida är ett slags råd eller information. Men vad händer om systemet skulle sättas ihop med ett uppvärmningssystem i en massa bostäder? Då kan en prediktion leda till att beslut att slå på värmen. Vem blir ansvarig när värmen inte slås på en kall natt? Under vilka omständigheter skulle ni vara bekväma med att stå bakom ett sådant system?

---

## Innan ni går på lunch

- [ ] Arbetsbladet är ifyllt och committat.
- [ ] **En** av de fyra frågorna är utvald till den fråga ni ska presentera på torsdag under 2-3 minuter.
- [ ] Alla i gruppen har läst alla svar: vem som helst av er kan få frågan på torsdag.
