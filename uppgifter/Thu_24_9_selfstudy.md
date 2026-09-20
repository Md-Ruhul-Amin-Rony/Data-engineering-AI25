# Torsdag 24/9 — liten lokal tjänst

Arbeta med detta först när feature-pipelinen och träningssteget är i ordning.

## 1. Ladda en specifik modellversion

Tjänsten ska använda en bestämd modellversion från Hugging Face, till exempel
`v1`. 

## 2. Börja med `/health`

Skapa en liten FastAPI-tjänst där `/health` svarar lokalt. Ett bra svar
innehåller till exempel:

- att tjänsten kör,
- vilken modellversion den laddade,
- vilket git-commit koden kommer från, om ni har den informationen.

Testa lokalt med webbläsare eller `curl`.

## 3. Om ni hinner

Bygg en Docker-image lokalt. `/predict`, Render, publik URL och
prediktionslogg är nästa steg och är inte ett krav i dag.

## Målbild

**Minimiläge:** modellen kan laddas lokalt, eller blockeraren är väl beskriven.

**Idealisk målbild:** `/health` fungerar lokalt med en pinnad modellversion och
en Docker-image bygger.
