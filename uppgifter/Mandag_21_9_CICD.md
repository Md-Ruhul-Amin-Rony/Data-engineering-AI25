# Måndag 21/9 — få CI att köra på en pull request

Målet är inte en stor pipeline. Målet är att GitHub automatiskt kontrollerar
kod innan den mergas. Börja efter genomgången om CI/CD på måndagen. Arbetet
görs i studiotiden och kan fortsätta på tisdagen, inte som kvällsarbete.

1. Kopiera `ci_starter.yml` till `.github/workflows/ci.yml`.
2. Anpassa kommandona om ert repo behöver det.
3. Öppna en liten PR från verkligt projektarbete.
4. Kontrollera att workflowen körs på pull request.
5. Rätta fel tills tester och linting är gröna.

Om ert repo använder andra kommandon än `uv run pytest` eller
`uv run ruff check .`, byt dem och skriv kort varför i PR:en.

## Viktigt

- En workflow som bara körs på `push` kontrollerar inte er PR.
- Slå på branch protection om ni har behörighet, så att en grön CI-körning
  krävs före merge.
- Lägg aldrig tokens eller anslutningssträngar i workflow-filen.

## Målbild

**Minimiläge:** en PR har en CI-körning och ni förstår varför den blev grön
eller röd.

**Idealisk målbild:** CI krävs före merge.
