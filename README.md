# Rampart Docs

Mintlify documentation for [rampart-monad](https://github.com/RampartLabs/rampart-monad).

**Live:** `https://docs.rampartlabs.xyz`

## Local Preview

```bash
npm install -g mintlify
mintlify dev
# → http://localhost:3000
```

## Structure

```
rampart-docs/
├── docs.json          ← Mintlify config (nav, colors, theme)
├── introduction.mdx
├── quickstart.mdx
├── logo/
├── sdk/
│   ├── dex/           (14 pages)
│   ├── lending/       (15 pages)
│   ├── lst/           (8 pages)
│   ├── perps/         (4 pages)
│   ├── yield/         (7 pages)
│   ├── oracles/
│   ├── aggregators/
│   └── ai-agent/
├── api/               (5 pages)
└── examples/          (3 pages)
```

## Deploy

Connect this repo to [mintlify.com](https://mintlify.com) → auto-deploys on every push to `main`.
