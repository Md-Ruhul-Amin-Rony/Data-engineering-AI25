# Onsdagens självstudier: Git-överlevnadskit

Bygger vidare på tisdagens session, då du skapade en branch, redigerade,
pushade och öppnade en pull request mot övningsrepot, samt löste en
sammanslagningskonflikt (merge conflict) i en sandlåda.

Fungerar i Codespaces eller på din egen dator. Allt du gör idag körs lokalt i
en tillfällig mapp — inget du gör här påverkar ett delat repo.

## Varför just detta?

Git är inte ett av kursens lärandemål. Det är ett verktyg du behöver för att
kunna arbeta i team under projektet. Tisdagen täckte flödet du kommer använda varje dag: branch, commit, push,
pull request, granskning. Idag täcker vi de två situationerna där det flödet
går fel och du behöver ta dig ur det.

## Kärnuppgifter (gör båda)

### 1. Stash — "Jag är halvvägs in i något och behöver byta branch"

Kör `stash.sh` (ligger i den här mappen). Det skapar ett tillfälligt repo med
oavslutat arbete i.

Dina uppgifter:

1. Stasha ändringarna.
2. Skapa och byt till en ny branch.
3. Applicera de stashade ändringarna på den nya branchen.

Det här dyker upp hela tiden i verkligt arbete: du är mitt i en redigering,
en lagkamrat ber dig titta på något på en annan branch, och du är inte redo
att committa det du har.

### 2. Amend — "den där committen blev fel"

Kör `amend-reset.sh` (ligger i den här mappen). Det skapar ett tillfälligt
repo där den senaste committen är fel.

Dina uppgifter:

1. Fixa den med `git commit --amend` — antingen meddelandet eller
   innehållet.
2. Titta sedan på `git log` och bekräfta att du förstår vad som ändrades.

Nästan alltid handlar det om ett stavfel i commit-meddelandet eller en fil
du glömde `git add`. Båda fixas på samma sätt.

**En regel:** amenda bara commits du inte redan har pushat. Amend skriver om
historiken, och att skriva om historik som någon annan redan har "pullat" kommer att skapa problem för dina samarbetspartners. Om den redan är
pushad, gör en ny commit istället.

## Om du har lösa trådar från tisdagen

- Om din pull request inte är mergad än, avsluta den.
- Om du inte har granskat din partners pull request, gör det nu.

## Förberedelse inför torsdag (~15 min)

På torsdag bygger ni er första riktiga datapipeline: en datainhämtningstjänst
(ingestion service) och en databas som körs tillsammans.

Läs kort om **varför man skulle vilja köra mer än en container samtidigt**.
Du har redan byggt en enskild container förra veckan. Torsdagens uppsättning
har en API-container och en Postgres-container som behöver hitta varandra,
starta i rätt ordning och dela ett nätverk. Kom med en ungefärlig bild av
vilket problem `docker-compose` löser. Du behöver inte kunna syntaxen.

## Frivilligt

`restore-reset.sh` finns också i den här mappen. **Gör bara uppgift 1** — att
återställa ostagade ändringar med `git restore`.

Hoppa över uppgift 2. 

## Vi hörs igen

Inget att lämna in. Om något inte fungerade, ta med det till torsdag morgon. De första tjugo minuterna är avsatta för precis det.
