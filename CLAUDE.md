# rampart-docs

## Що це

Документація для `rampart-monad` SDK на базі Mintlify.
MDX файли з живими прикладами коду.

## Технічний стек

- Mintlify (theme: "mint", `docs.json`)
- MDX (Markdown + JSX компоненти)
- Без npm/build — Mintlify сам збирає

## Структура

```
docs.json           — конфіг Mintlify (тема, навігація, логотипи)
introduction.mdx    — головна сторінка
quickstart.mdx      — старт за 2 хвилини
protocols.mdx       — огляд всіх протоколів
sdk/
  overview.mdx
  price.mdx
  portfolio.mdx
  tvl.mdx
  markets.mdx
  dex/
  lst/
  lending/
  oracles/
  perps/
  yield/
  aggregators/
  ai-agent/
api/                — документація REST API ендпоінтів
logo/               — SVG логотипи (rampart-dark.svg, rampart-light.svg, favicon.svg)
```

## Бренд

- Primary: `#836ef9`
- Light: `#a893fb`
- Dark: `#6247e8`

## Важливі правила

- Документація відображає поточний стан `rampart-monad` SDK
- При додаванні нового протоколу/функції в SDK — оновлювати відповідний MDX
- Приклади коду мають бути живими та актуальними

## Команди

Mintlify dev (локально):
```bash
npx mintlify dev
```

## Як пов'язана з іншими

- Документує **rampart-monad** SDK та **rampart-api** ендпоінти
- **rampart-site** посилається на цю документацію
- **rampart-chainlens** — не документується тут (окремий продукт)

## Git

```
user.name  = 0xNickyTan
user.email = m225dw@gmail.com
SSH host   = github-rampart  (для RampartLabs організації)
remote     = git@github-rampart:RampartLabs/rampart-docs.git
```

Всі коміти та пуші тільки від `0xNickyTan`. Інший акаунт не використовувати.

## Поточний статус

MDX файли готові. Деплоїться через Mintlify hosting.
Є `rampart-whitepaper.pdf` і скріншоти дашборду у корені.
