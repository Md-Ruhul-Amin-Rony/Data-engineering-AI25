# Måndag 7/9: Basmodell och Hugging Face

Idag ska ni förbereda er inför torsdagens arbete med modellregister.

## 1. Kör basmodellen

I projektets startrepo:

```bash
uv run python model/train.py
```

Kontrollera att skriptet kör klart och skapar en modellfil i `model/`.

Skriv ner:

- vilket elområde och target ni använder
- vilket mått (*metric*) som skrivs ut, till exempel R² eller MAE
- vilket commit ni körde från

För att hitta commit:

```bash
git log -1 --oneline
```

Kopiera raden som skrivs ut, till exempel `a1b2c3d fixa feature-beräkning`.

Om skriptet inte kör: skriv ner felmeddelandet och vad ni redan har provat. Ta med det till tisdagen eller onsdagens handledning.

## 2. Förbered modellregistret

Välj en person i gruppen som ansvarar för modellregistret.

Den personen ska:

1. Skapa ett konto på [Hugging Face](https://huggingface.co).
2. Bekräfta e-postadressen.
3. Skapa ett privat model repository för gruppen, till exempel `elpris-se3-team-3`.

Ladda inte upp någon token till GitHub och lägg inte token i någon fil som committas.

Om kontot eller repot inte blir klart idag är det okej. Vi gör själva uppladdningen tillsammans på torsdag.

## 3. Inför tisdag: vad kostar det?

Välj en av AWS, Azure eller Google Cloud. Leta upp följande på leverantörens egna prissidor:

1. Pris per månad för en liten container som kör ett API med mycket låg trafik. Kan den skala till noll?
2. Pris per månad för minsta managed PostgreSQL-databas.
3. Pris för att lagra 10 GB och för att föra ut 10 GB data ur leverantörens nät.
4. Vad ingår i free tier, och vad händer när den tar slut?

Skriv ner svaren och länkarna till prissidorna. Ta med dem till tisdagens lektion.

## Klart när

- [ ] `train.py` har körts och en modellfil finns i `model/`
- [ ] gruppen har sparat mått och commit
- [ ] en ansvarig för Hugging Face är utsedd
- [ ] Hugging Face-konto och privat model repo finns, om möjligt
- [ ] gruppen har med sig fyra molnpriser till tisdag
