# Tisdag 22/9 — forecastfeatures och träningspipeline

Arbeta med nästa steg i den här ordningen. Börja inte med FastAPI eller Render
förrän feature- och träningskedjan fungerar bra.

## 1. Använd forecast i feature-pipelinen

`raw__weather` innehåller forecast-rådata och `stg__forecast` visar
normaliserade värden. Uppdatera `feature_pipeline.py` så att den använder
prognostiserad temperatur och vind när den bygger feature-raden för kommande
dag.

## 2. Träna från featuretabellen

När `feat__daily` fungerar:

1. Låt `train.py` läsa färdiga rader från `feat__daily`.
2. Registrera den tränade modellen på Hugging Face.
3. Spara vilken modellversion som ska användas senare.

`train.py` ska inte längre beräkna features direkt från staging-tabellerna.

## 3. Commita

Commita och pusha det ni har gjort, även om nästa steg återstår. Skriv kort i
PR eller commit vad som fungerar och vad som fortfarande blockerar.

## Målbild

**Minimiläge:** forecastlogiken eller träningspipeline-steget har gått framåt,
och nästa steg är tydligt.

**Idealisk målbild:** morgondagens feature-rad finns i `feat__daily`, `train.py`
läser därifrån och en modellversion är registrerad på Hugging Face.
