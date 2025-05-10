# FastAPI CMS

![FastAPI CMS Logo](static/img/logo.png)

Moderní, rychlý a flexibilní systém pro správu obsahu postavený na FastAPI a SQLModel.

## O projektu

FastAPI CMS je open-source systém pro správu obsahu, který kombinuje rychlost a jednoduchost FastAPI s flexibilitou SQLModel pro vytváření moderních webových aplikací. Tento CMS je navržen s důrazem na výkon, bezpečnost a snadnou rozšiřitelnost.

### Klíčové funkce

- **Moderní technologie**: Postaveno na FastAPI, SQLModel a Jinja2
- **Vysoký výkon**: Asynchronní zpracování požadavků pro maximální rychlost
- **Flexibilní správa obsahu**: Podpora stránek, článků a modulárních bloků
- **Kategorizace obsahu**: Oddělené kategorie pro stránky, články a bloky
- **Uživatelské role**: Podpora pro administrátory, editory a běžné uživatele
- **JWT autentizace**: Bezpečné přihlašování a správa relací
- **Responzivní design**: Moderní uživatelské rozhraní postavené na Bootstrap 5
- **SEO optimalizace**: Podpora meta tagů, URL friendly adres a klíčových slov

## Technologie

- **Backend**: FastAPI, SQLModel, Pydantic
- **Databáze**: SQLite (s možností přechodu na PostgreSQL nebo MySQL)
- **Autentizace**: JWT (JSON Web Tokens)
- **Frontend**: Bootstrap 5, Jinja2, HTMX, Font Awesome
- **Deployment**: Uvicorn

### Proč HTMX místo Reactu?

Náš CMS využívá HTMX místo tradičních JavaScript frameworků jako React, Vue nebo Angular. Zde jsou hlavní výhody tohoto přístupu:

- **Jednodušší architektura**: HTMX umožňuje vytvářet dynamické aplikace bez nutnosti psát komplexní JavaScript kód nebo používat složité build systémy.
- **Menší velikost**: HTMX je pouze ~14kB (gzipped), zatímco React s ReactDOM je ~40kB, což vede k rychlejšímu načítání stránek.
- **Žádný kontext přepínání**: Vývojáři pracují pouze s HTML, CSS a backend kódem, bez nutnosti přepínat mezi různými paradigmaty a jazyky.
- **Progresivní vylepšení**: HTMX umožňuje postupně vylepšovat existující HTML, což usnadňuje integraci do stávajících projektů.
- **Serverový rendering**: Veškeré vykreslování probíhá na serveru, což zjednodušuje SEO a zlepšuje výkon na méně výkonných zařízeních.
- **Méně JavaScript kódu**: Méně kódu znamená méně chyb, lepší udržovatelnost a snazší onboarding nových vývojářů.
- **Hypermedia-driven aplikace**: HTMX podporuje HATEOAS princip, což vede k intuitivnějšímu návrhu API.

## Instalace

### Požadavky

- Python 3.8+
- pip

### Postup instalace

1. Klonujte repozitář:
   ```bash
   git clone https://github.com/dnatron/FastApi-CMS.git
   cd FastApi-CMS
   ```

2. Vytvořte a aktivujte virtuální prostředí:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Na Windows: venv\Scripts\activate
   ```

3. Nainstalujte závislosti:
   ```bash
   pip install -r requirements.txt
   ```

4. Spusťte aplikaci:
   ```bash
   uvicorn app:app --reload
   ```

5. Otevřete prohlížeč a přejděte na adresu:
   ```
   http://localhost:8000
   ```

## Použití

### Přihlášení administrátora

Po prvním spuštění se automaticky vytvoří administrátorský účet:
- **Uživatelské jméno**: admin
- **Heslo**: admin

> **Důležité**: Po prvním přihlášení změňte heslo administrátora!

### Správa obsahu

- **Stránky**: Vytvářejte a upravujte statické stránky
- **Blog**: Publikujte články s podporou kategorií a tagů
- **Bloky**: Vytvářejte modulární bloky obsahu pro použití na stránkách
- **Kategorie**: Organizujte obsah do kategorií
- **Uživatelé**: Spravujte uživatelské účty a role

## Struktura projektu

```
FastApi-CMS/
├── database/         # Konfigurace databáze
├── models/           # SQLModel modely
├── routers/          # FastAPI routery
├── security/         # Autentizace a autorizace
├── static/           # Statické soubory (CSS, JS, obrázky)
├── templates/        # Jinja2 šablony
├── main.py           # Hlavní aplikační soubor
└── requirements.txt  # Seznam závislostí
```

## Roadmapa

- [ ] Administrační rozhraní pro správu obsahu
- [ ] Editor WYSIWYG pro pohodlnější úpravy
- [ ] Systém pluginů pro rozšíření funkcionality
- [ ] Podpora více jazyků
- [ ] Integrace s CDN pro správu médií
- [ ] API dokumentace pomocí Swagger UI
- [ ] Migrace na PostgreSQL pro produkční nasazení

## Přispívání

Příspěvky jsou vítány! Pokud chcete přispět k vývoji FastAPI CMS, postupujte podle těchto kroků:

1. Forkněte repozitář
2. Vytvořte novou větev (`git checkout -b feature/amazing-feature`)
3. Proveďte změny a commitněte je (`git commit -m 'Add some amazing feature'`)
4. Pushněte do větve (`git push origin feature/amazing-feature`)
5. Otevřete Pull Request

## Licence

Distribuováno pod licencí MIT. Viz `LICENSE` soubor pro více informací.

## Kontakt a informace

Denveloper: [https://www.dnatron.com](https://www.dnatron.com)

CMS website: [https://www.dnatron.com/fastapi-cms](https://www.dnatron.com/fastapi-cms)

Odkaz na projekt: [https://github.com/dnatron/FastApi-CMS](https://github.com/dnatron/FastApi-CMS)
