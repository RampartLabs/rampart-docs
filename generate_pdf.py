from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.colors import HexColor

OUT = "D:/GitHub/rampart-docs/rampart-whitepaper.pdf"
W, H = A4

PURPLE      = HexColor('#836EF9')
PURPLE_DARK = HexColor('#5B4BD4')
PURPLE_SOFT = HexColor('#EDE9FF')
BG_DARK     = HexColor('#0D0B1A')
BG_SECTION  = HexColor('#F7F6FF')
GRAY        = HexColor('#6B7280')
GRAY_LIGHT  = HexColor('#E5E7EB')
DARK        = HexColor('#111827')
WHITE       = colors.white
CODE_BG     = HexColor('#1E1B2E')
CODE_FG     = HexColor('#C4B5FD')

def S(name, **kw):
    return ParagraphStyle(name, **kw)

sTitle    = S('sTitle',    fontName='Helvetica-Bold',   fontSize=36, leading=44, textColor=WHITE,       alignment=TA_LEFT,    spaceAfter=6)
sSubtitle = S('sSubtitle', fontName='Helvetica',        fontSize=15, leading=20, textColor=HexColor('#C4B5FD'), alignment=TA_LEFT, spaceAfter=4)
sMeta     = S('sMeta',     fontName='Helvetica',        fontSize=9,  leading=13, textColor=HexColor('#9CA3AF'), alignment=TA_LEFT)
sH1       = S('sH1',       fontName='Helvetica-Bold',   fontSize=20, leading=26, textColor=DARK,        spaceBefore=12, spaceAfter=7)
sH2       = S('sH2',       fontName='Helvetica-Bold',   fontSize=14, leading=18, textColor=PURPLE_DARK, spaceBefore=10, spaceAfter=5)
sH3       = S('sH3',       fontName='Helvetica-Bold',   fontSize=11, leading=15, textColor=DARK,        spaceBefore=7,  spaceAfter=3)
sBody     = S('sBody',     fontName='Helvetica',        fontSize=10, leading=16, textColor=DARK,        alignment=TA_JUSTIFY, spaceAfter=6)
sBodyL    = S('sBodyL',    fontName='Helvetica',        fontSize=10, leading=16, textColor=DARK,        alignment=TA_LEFT,    spaceAfter=4)
sBullet   = S('sBullet',   fontName='Helvetica',        fontSize=10, leading=15, textColor=DARK,        leftIndent=10,  spaceAfter=3)
sNote     = S('sNote',     fontName='Helvetica-Oblique',fontSize=9,  leading=13, textColor=GRAY,        leftIndent=12,  spaceAfter=4)
sTH       = S('sTH',       fontName='Helvetica-Bold',   fontSize=9,  leading=12, textColor=WHITE,       alignment=TA_CENTER)
sTD       = S('sTD',       fontName='Helvetica',        fontSize=9,  leading=12, textColor=DARK,        alignment=TA_LEFT)
sTDc      = S('sTDc',      fontName='Helvetica',        fontSize=9,  leading=12, textColor=DARK,        alignment=TA_CENTER)
sCover    = S('sCover',    fontName='Helvetica',        fontSize=12, leading=17, textColor=HexColor('#C4B5FD'), alignment=TA_LEFT, spaceAfter=4)
sFooter   = S('sFooter',   fontName='Helvetica',        fontSize=8,  leading=11, textColor=GRAY,        alignment=TA_CENTER)

def cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG_DARK)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(PURPLE_DARK)
    canvas.rect(0, H - 6*mm, W, 6*mm, fill=1, stroke=0)
    canvas.setFillColor(HexColor('#150F2A'))
    canvas.circle(W + 30*mm, H + 30*mm, 110*mm, fill=1, stroke=0)
    canvas.circle(-15*mm, -25*mm, 70*mm, fill=1, stroke=0)
    canvas.setStrokeColor(HexColor('#1F1B38'))
    canvas.setLineWidth(0.4)
    for y in range(0, int(H), int(18*mm)):
        canvas.line(0, y, W, y)
    for x in range(0, int(W), int(18*mm)):
        canvas.line(x, 0, x, H)
    canvas.restoreState()

def normal_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PURPLE)
    canvas.rect(0, H - 3*mm, W, 3*mm, fill=1, stroke=0)
    canvas.setFillColor(GRAY_LIGHT)
    canvas.rect(0, 0, W, 11*mm, fill=1, stroke=0)
    canvas.setFillColor(GRAY)
    canvas.setFont('Helvetica', 7)
    canvas.drawString(20*mm, 4*mm, 'Rampart SDK  -  Technical Whitepaper v0.1.0  -  April 2026')
    canvas.drawRightString(W - 20*mm, 4*mm, f'Page {doc.page}')
    canvas.setFillColor(PURPLE)
    canvas.rect(0, 11*mm, 3*mm, H - 14*mm, fill=1, stroke=0)
    canvas.restoreState()

def page_cb(canvas, doc):
    if doc.page == 1:
        cover_bg(canvas, doc)
    else:
        normal_bg(canvas, doc)

def rule():
    return HRFlowable(width='100%', thickness=1, color=PURPLE_SOFT, spaceAfter=4, spaceBefore=4)

def section_header(text):
    data = [[Paragraph(text, S('sh', fontName='Helvetica-Bold', fontSize=12,
                                textColor=WHITE, spaceAfter=0))]]
    t = Table(data, colWidths=[170*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), PURPLE),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 14),
    ]))
    return [Spacer(1, 5*mm), t, Spacer(1, 5*mm)]

def code_box(text):
    rows = []
    for line in text.strip().split('\n'):
        safe = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        safe = safe.replace(' ', '&nbsp;')
        rows.append([Paragraph(safe, S('cb', fontName='Courier', fontSize=8,
                                       leading=12, textColor=CODE_FG, spaceAfter=0))])
    inner = Table(rows, colWidths=[166*mm])
    inner.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), CODE_BG),
        ('TOPPADDING',    (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
    ]))
    wrap = Table([[inner]], colWidths=[170*mm])
    wrap.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), CODE_BG),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 2),
        ('RIGHTPADDING',  (0,0), (-1,-1), 2),
    ]))
    return [Spacer(1, 2*mm), wrap, Spacer(1, 4*mm)]

def tbl(headers, rows, widths):
    hrow = [Paragraph(h, sTH) for h in headers]
    brows = []
    for row in rows:
        brows.append([Paragraph(str(c), sTD if i == 0 else sTDc)
                      for i, c in enumerate(row)])
    t = Table([hrow] + brows, colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  PURPLE),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, BG_SECTION]),
        ('GRID',          (0,0), (-1,-1), 0.4, GRAY_LIGHT),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('ALIGN',         (0,1), (0,-1),  'LEFT'),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 7),
        ('RIGHTPADDING',  (0,0), (-1,-1), 7),
    ]))
    return [t, Spacer(1, 5*mm)]

def stat_row(items):
    cells = []
    for val, label, sub in items:
        c = Table([
            [Paragraph(val,   S('sv', fontName='Helvetica-Bold', fontSize=20, textColor=PURPLE, spaceAfter=2))],
            [Paragraph(label, S('sl', fontName='Helvetica-Bold', fontSize=9,  textColor=DARK,   spaceAfter=1))],
            [Paragraph(sub,   S('ss', fontName='Helvetica',      fontSize=8,  textColor=GRAY))],
        ], colWidths=[38*mm])
        c.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), PURPLE_SOFT),
            ('TOPPADDING',    (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ]))
        cells.append(c)
    row = Table([cells], colWidths=[42*mm] * len(items))
    row.setStyle(TableStyle([
        ('LEFTPADDING',  (0,0), (-1,-1), 1),
        ('RIGHTPADDING', (0,0), (-1,-1), 1),
    ]))
    return [row, Spacer(1, 5*mm)]

# ─── Story ───────────────────────────────────────────────────────────────────
s = []

# ── Cover ────────────────────────────────────────────────────────────────────
s.append(Spacer(1, 36*mm))

badge = Table([[Paragraph('TECHNICAL WHITEPAPER  v0.1.0',
    S('bv', fontName='Helvetica-Bold', fontSize=9, textColor=PURPLE))]],
    colWidths=[60*mm])
badge.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), HexColor('#1A1530')),
    ('TOPPADDING',    (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING',   (0,0), (-1,-1), 10),
    ('BOX',           (0,0), (-1,-1), 1, PURPLE),
]))
s.append(badge)
s.append(Spacer(1, 10*mm))
s.append(Paragraph('Rampart SDK', sTitle))
s.append(Spacer(1, 3*mm))
s.append(Paragraph('The Unified DeFi Interface for Monad', sSubtitle))
s.append(Spacer(1, 8*mm))

stripe = Table([['']], colWidths=[48*mm], rowHeights=[3])
stripe.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), PURPLE)]))
s.append(stripe)
s.append(Spacer(1, 8*mm))

s.append(Paragraph('55+ protocols. 41 AI tools. One TypeScript import.', sCover))
s.append(Spacer(1, 10*mm))

cstats = [('55+','Protocols','DEX, Lending, LST, Perps, Yield'),
          ('41','AI Tools','Vercel AI SDK v6 tools'),
          ('~$200M','TVL Tracked','Lending + LST aggregate'),
          ('400ms','Block Time','Monad Mainnet native')]
for val, lbl, sub in cstats:
    ct = Table([
        [Paragraph(val, S('cv', fontName='Helvetica-Bold', fontSize=20, textColor=PURPLE, spaceAfter=2))],
        [Paragraph(lbl, S('cl', fontName='Helvetica-Bold', fontSize=9,  textColor=HexColor('#C4B5FD'), spaceAfter=1))],
        [Paragraph(sub, S('cs', fontName='Helvetica',      fontSize=8,  textColor=HexColor('#6B7280')))],
    ], colWidths=[32*mm])
    ct.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), HexColor('#1A1530')),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('BOX',           (0,0), (-1,-1), 0.5, HexColor('#2D2550')),
    ]))

cs_items = []
for val, lbl, sub in cstats:
    ct = Table([
        [Paragraph(val, S(f'cv{val}', fontName='Helvetica-Bold', fontSize=20, textColor=PURPLE, spaceAfter=2))],
        [Paragraph(lbl, S(f'cl{val}', fontName='Helvetica-Bold', fontSize=9,  textColor=HexColor('#C4B5FD'), spaceAfter=1))],
        [Paragraph(sub, S(f'cs{val}', fontName='Helvetica',      fontSize=8,  textColor=HexColor('#6B7280')))],
    ], colWidths=[32*mm])
    ct.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), HexColor('#1A1530')),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('BOX',           (0,0), (-1,-1), 0.5, HexColor('#2D2550')),
    ]))
    cs_items.append(ct)
cs_grid = Table([cs_items], colWidths=[36*mm]*4)
cs_grid.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),2),('RIGHTPADDING',(0,0),(-1,-1),2)]))
s.append(cs_grid)

s.append(Spacer(1, 38*mm))
s.append(Paragraph('Published: April 2026   |   Version 0.1.0   |   npm: rampart-monad', sMeta))
s.append(Paragraph('https://github.com/andrienkoj7crypto/rampart-monad', sMeta))
s.append(PageBreak())

# ── 01 Abstract ──────────────────────────────────────────────────────────────
s += section_header('01   ABSTRACT')
s.append(Paragraph(
    'Rampart is an open-source TypeScript SDK that provides a unified, typed interface to 55+ DeFi '
    'protocols deployed on Monad Mainnet. It eliminates the integration overhead of working with '
    'heterogeneous on-chain ABIs by exposing a consistent function API across DEXes, lending markets, '
    'liquid staking tokens, perpetuals, yield vaults, and price oracles.',
    sBody))
s.append(Paragraph(
    'Beyond raw protocol access, Rampart ships a three-layer architecture: standalone protocol '
    'functions, an object-oriented Rampart client class, and a first-class AI agent layer built '
    'on the Vercel AI SDK v6. The agent layer exposes 41 structured tools that any LLM with '
    'tool-calling support can use to query and reason over live Monad DeFi data autonomously.',
    sBody))
s.append(Paragraph(
    'The SDK ships as ESM + CJS + TypeScript declarations, requires Node.js 18+ and TypeScript 5+, '
    'and connects to Monad Mainnet with zero chain configuration from the developer.',
    sBody))
s.append(rule())
s.append(Spacer(1, 2*mm))

# ── 02 Problem Statement ──────────────────────────────────────────────────────
s += section_header('02   PROBLEM STATEMENT')
s.append(Paragraph('The DeFi Integration Tax', sH2))
s.append(Paragraph(
    'Building on a DeFi ecosystem from scratch means writing bespoke integrations for every '
    'protocol: parsing ABIs, handling multicall batching, managing RPC quirks, normalizing '
    'numeric formats (wei, ray, wad), and maintaining correctness as contracts upgrade. '
    'On Monad this is compounded by a fast-moving protocol landscape where 55+ protocols '
    'have launched with varying architectures.',
    sBody))
s.append(Paragraph('Specific pain points solved by Rampart:', sH3))
for b in [
    'ABI management: every protocol requires its own ABI files and type generation.',
    'RPC quirks: simulateContract is required for Uniswap QuoterV2; eth_getLogs from block 0 fails on Morpho.',
    'Numeric normalization: Euler APR = interestRate() / 1e27 * 31_536_000. Each protocol differs.',
    'Oracle gaps: Chainlink has no MON/USD feed; Pyth feed ID is unconfirmed; Kuru DEX is currently most reliable.',
    'AI integration: wiring LLM tool schemas for 55+ protocols individually requires significant boilerplate.',
]:
    s.append(Paragraph(f'  -  {b}', sBullet))
s.append(rule())
s.append(Spacer(1, 2*mm))

# ── 03 Architecture ───────────────────────────────────────────────────────────
s += section_header('03   ARCHITECTURE')
s.append(Paragraph(
    'Rampart is structured in three layers, each building on the one below it.',
    sBody))

for badge_txt, title, desc in [
    ('Layer 1', 'Protocol Functions',
     'Individual async TypeScript functions, one per protocol action. Tree-shakeable. '
     'Uses publicClient from chain.ts, pre-configured for Monad (chain ID 143, rpc.monad.xyz).'),
    ('Layer 2', 'Rampart Class',
     'Object-oriented client bundling all protocol functions as methods. Ideal for backends '
     'and services where a single instantiated client is preferred over named imports.'),
    ('Layer 3', 'RampartAgent',
     'Extends Rampart and wraps every function as a Vercel AI SDK v6 tool(). Each tool has '
     'an inputSchema (Zod) and execute function. Pass agent.tools directly to generateText.'),
]:
    row = Table([
        [Paragraph(badge_txt, S(f'lb{badge_txt}', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
         Paragraph(f'<b>{title}</b>', S(f'lt{title}', fontName='Helvetica-Bold', fontSize=11, textColor=DARK)),
         Paragraph(desc, S(f'ld{title}', fontName='Helvetica', fontSize=9, leading=14, textColor=DARK))],
    ], colWidths=[18*mm, 36*mm, 116*mm])
    row.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (0,0),  PURPLE),
        ('BACKGROUND',    (1,0), (-1,0), PURPLE_SOFT),
        ('ALIGN',         (0,0), (0,0),  'CENTER'),
        ('VALIGN',        (0,0), (-1,-1),'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('BOX',           (0,0), (-1,-1), 0.4, GRAY_LIGHT),
    ]))
    s.append(row)
    s.append(Spacer(1, 3*mm))

s.append(Spacer(1, 2*mm))
s.append(Paragraph('Layer 1 - Direct function imports', sH3))
s += code_box("""import { getBestSwapRoute, getEulerVaults, getAllLSTStats } from 'rampart-monad'

const route  = await getBestSwapRoute(MON, USDC, '1000000000000000000')
const vaults = await getEulerVaults()     // 108 Euler V2 vaults with live APR
const lsts   = await getAllLSTStats()     // All 5 LSTs compared by APR + TVL""")

s.append(Paragraph('Layer 3 - AI Agent', sH3))
s += code_box("""import { RampartAgent } from 'rampart-monad'
import { generateText } from 'ai'
import { anthropic } from '@ai-sdk/anthropic'

const { text } = await generateText({
  model: anthropic('claude-3-5-sonnet-20241022'),
  tools: new RampartAgent().tools,
  prompt: 'What is the best yield for 10,000 USDC on Monad right now?',
  maxSteps: 5,
})""")

s.append(rule())
s.append(Spacer(1, 2*mm))

# ── 04 Protocol Coverage ──────────────────────────────────────────────────────
s += section_header('04   PROTOCOL COVERAGE')
s += stat_row([
    ('14', 'DEX Protocols',    'Orderbooks, AMMs, Aggregators'),
    ('14', 'Lending Markets',  'Aave, Euler, Morpho, CDP, RWA'),
    ('9',  'LST & Vaults',     'aprMON, sMON, gMON and more'),
    ('4',  'Perps Venues',     'Monday, Narwhal, Pingu, Purps'),
])

s.append(Paragraph('4.1  Decentralized Exchanges', sH2))
s += tbl(
    ['Protocol', 'Type', 'TVL', 'Function'],
    [['Kuru',           'Orderbook AMM',           '~$5M',   'getKuruPools()'],
     ['Uniswap V3',     'Concentrated Liquidity',  '~$10M',  'getUniswapPools()'],
     ['Uniswap V4',     'V4 Hooks AMM',            '~$2M',   'getUniswapV4Pools()'],
     ['PancakeSwap',    'V3 Conc. Liquidity',      '~$8M',   'getPancakeSwapPools()'],
     ['Clober',         'On-chain Orderbook',      '~$1M',   'getCloberBooks()'],
     ['iZiSwap',        'Discrete Liquidity',      '~$1M',   'getIziPools()'],
     ['Capricorn',      'Uniswap V3 Fork',         '~$1M',   'getCapricornPrice()'],
     ['KyberSwap',      'DEX Aggregator',          '~$300K', 'getKyberSwapRoute()'],
     ['Swaap',          'Market-Maker DEX',        '~$500K', 'getSwaapTVL()'],
     ['WooFi',          'Proactive Market Maker',  '~$1M',   'getWooFiPrice()'],
     ['LFJ (Trader Joe)','DLMM Liquidity Book',   '~$2M',   'getLFJPools()'],
     ['OpenOcean',      'DEX Aggregator (REST)',   '~$200K', 'getOpenOceanRoute()'],
     ['Bean',           'DLMM DEX',               '~$500K', 'getBeanPairs()'],],
    [36*mm, 48*mm, 22*mm, 64*mm]
)

s.append(Paragraph('4.2  Lending Protocols', sH2))
s += tbl(
    ['Protocol', 'Type', 'TVL', 'Function'],
    [['Curvance',    'Multi-Collateral',         '~$58.9M','getCurvanceMarkets()'],
     ['Euler V2',    'Permissionless (108 vaults)','~$20M','getEulerVaults()'],
     ['Neverland',   'Aave V3 Fork',             '~$15M',  'getLendingRates()'],
     ['Folks Finance','Cross-Chain spoke/hub',   '~$8M',   'getFolksMarkets()'],
     ['Morpho',      'MetaMorpho / Blue',        '~$5M',   'getMorphoVaults()'],
     ['Sumer Money', 'Compound V2 Fork',         '~$4M',   'getSumerMarkets()'],
     ['Nabla',       'Single-Sided AMM',         '~$3M',   'getNablaPools()'],
     ['Sherpa',      'Delta-Neutral USDC',       '~$3M',   'getSherpaVaults()'],
     ['TownSquare',  'Cross-Chain hub',          '~$2M',   'getTownSquareMarkets()'],
     ['Accountable', 'Undercollateralized',      '~$2M',   'getAccountableVaults()'],
     ['Multipli',    'RWA Yield Vaults',         '~$1M',   'getMultipliVault()'],
     ['Timeswap',    'Fixed-Maturity Options',   '~$500K', 'getTimeswapStats()'],
     ['Covenant',    'CDP / Structured',         '~$500K', 'getCovenantStats()'],
     ['LeverUp',     'Leveraged Perps',          '~$500K', 'getLeverUpStats()'],],
    [30*mm, 50*mm, 24*mm, 66*mm]
)

s.append(Paragraph('4.3  Liquid Staking Tokens', sH2))
s += tbl(
    ['Token', 'Protocol', 'APR', 'TVL', 'Function'],
    [['aprMON','aPriori','~8%',   '~$48M', 'getAPrioriLST()'],
     ['sMON',  'Magma',  '~7%',  '~$30M', 'getAllLSTStats()'],
     ['gMON',  'Kintsu', '~7.5%','~$25M', 'getAllLSTStats()'],
     ['shMON', 'FastLane','~6.5%','~$15M','getAllLSTStats()'],
     ['vshMON','Mellow', '~9%',  '~$19M', 'getMellowVaults()'],
     ['lagMON','Lagoon', '-',    '~$2M',  'getLagoonVaults()'],
     ['upMON', 'Upshift','-',    '~$3M',  'getUpshiftVaults()'],
     ['-',     'Beefy',  '-',    '~$2M',  'getBeefyVaults()'],
     ['ezMON', 'Renzo',  '-',    '~$500K','getRenzoStats()'],],
    [22*mm, 26*mm, 16*mm, 20*mm, 86*mm]
)

s.append(Paragraph('4.4  Perpetuals and Yield', sH2))
s += tbl(
    ['Protocol', 'Type', 'Function'],
    [['Monday Markets','GMX V2-style, multi-asset collateral', 'getMondayMarkets()'],
     ['Narwhal',       'Single-vault perpetuals',              'getNarwhalVault()'],
     ['Pingu Exchange','DataStore/Positions (GMX-like)',       'getPinguMarkets()'],
     ['Purps',         'Fully on-chain perpetual AMM',         'getPurpsMarkets()'],
     ['Enjoyoors',     'ERC4626 auto-compounding vaults',      'getEnjoyoorsVaults()'],
     ['Gearbox V3',    'Leveraged external deposits',          'getGearboxPools()'],
     ['Sablier',       'Token streaming / vesting',            'getSablierStream()'],
     ['Balancer V3',   'Weighted AMM pools',                   'getBalancerPools()'],
     ['Curve Finance', 'StableSwap stable pools',              'getCurvePools()'],
     ['nad.fun',       'Memecoin bonding curve launchpad',     'getNadFunTokens()'],],
    [36*mm, 72*mm, 62*mm]
)

s.append(rule())
s.append(Spacer(1, 2*mm))
s.append(PageBreak())

# ── 05 AI Agent ───────────────────────────────────────────────────────────────
s += section_header('05   AI AGENT LAYER')
s.append(Paragraph(
    'RampartAgent extends the Rampart class and wraps every SDK function as a Vercel AI SDK v6 '
    'tool. Passing agent.tools to generateText or streamText gives any LLM the ability to query '
    'live on-chain DeFi data autonomously across all 55+ protocols.',
    sBody))
s.append(Paragraph(
    'Each tool uses inputSchema: (Zod, Vercel AI SDK v6 API). Do not use parameters: which is '
    'the v5 API. The execute function delegates directly to the underlying RPC call with no '
    'added latency layer.',
    sBody))

s.append(Paragraph('5.1  Complete Tool Reference (41 tools)', sH2))
s += tbl(
    ['Tool', 'Description', 'Returns'],
    [['get_kuru_pools',          'Kuru DEX pool list',              'KuruPool[]'],
     ['get_kuru_price',          'MON spot price via Kuru',         'number'],
     ['get_token_price',         'Token price (any symbol)',        'TokenPrice'],
     ['get_uniswap_pools',       'Uniswap V3 active pools',        'Pool[]'],
     ['get_euler_vaults',        'All 108 Euler V2 vaults',        'EulerVault[]'],
     ['get_euler_best_supply',   'Highest-APR Euler vault',        'EulerVault'],
     ['get_neverland_rates',     'Neverland supply/borrow APY',    'LendingRate[]'],
     ['get_morpho_vaults',       'MetaMorpho vault list',          'MorphoVault[]'],
     ['get_all_lst_stats',       'All 5 LSTs: APR + TVL',          'LSTStats[]'],
     ['get_best_lst',            'Highest-APR liquid staking',     'LSTStats'],
     ['compare_lsts',            'Side-by-side LST comparison',    'LSTStats[]'],
     ['get_staking_apr',         'aPriori staking APR',            'StakingAPR'],
     ['get_best_swap_route',     'Best route across 6 DEXes',      'RouterResult'],
     ['get_all_swap_quotes',     'All DEX quotes for a pair',      'SwapRoute[]'],
     ['detect_arbitrage',        'DEX spread alerts >0.5%',        'ArbitrageAlert[]'],
     ['get_market_overview',     'Full ecosystem snapshot',        'MonadMarketOverview'],
     ['get_best_yields',         'Top yield opportunities',        'YieldOpportunity[]'],
     ['get_monad_tvl',           'Aggregate DeFi TVL',             'TVLBreakdown'],
     ['get_portfolio',           'Wallet portfolio snapshot',      'Portfolio'],
     ['get_token_balances',      'ERC20 token balances',           'TokenBalance[]'],
     ['get_euler_positions',     'Euler vault holdings',           'EulerPosition[]'],
     ['get_lst_positions',       'LST token holdings',             'LSTPosition[]'],
     ['get_verified_price',      'Cross-oracle price + confidence','VerifiedPrice'],
     ['get_prices',              'Batch oracle price query',       'OraclePrice[]'],
     ['detect_oracle_discrepancy','Source deviation flag',         'boolean'],
     ['get_lst_ratios',          'All LST/MON exchange rates',     'LSTRatios'],
     ['get_pancakeswap_pools',   'PancakeSwap V3 pools',           'PancakeSwapPair[]'],
     ['get_nadfun_stats',        'nad.fun launchpad stats',        'NadFunStats'],
     ['get_trending_memes',      'Trending memecoin list',         'MemeToken[]'],
     ['get_perp_markets',        'Perpetual market data',          'PerpMarket[]'],
     ['get_perp_tvl',            'Total perpetuals TVL',           'number'],
     ['get_curvance_markets',    'Curvance lending markets',       'CurvanceMarket[]'],
     ['get_best_yields_for_asset','Yields filtered by asset',      'YieldOpportunity[]'],
     ['get_uniswap_v4_pools',    'Uniswap V4 hook pools',          'UniswapV4Pool[]'],
     ['get_mellow_vaults',       'Mellow vshMON vaults',           'MellowVault[]'],
     ['get_market_intelligence', 'Full market intelligence',       'MonadMarketOverview'],],
    [56*mm, 70*mm, 44*mm]
)

s.append(Paragraph('5.2  Multi-Step Agent Example', sH2))
s += code_box("""import { RampartAgent } from 'rampart-monad'
import { generateText } from 'ai'
import { anthropic } from '@ai-sdk/anthropic'

const agent = new RampartAgent()

const { text, steps } = await generateText({
  model: anthropic('claude-3-5-sonnet-20241022'),
  tools: agent.tools,
  system: 'You are a Monad DeFi analyst.',
  prompt: 'Compare best LST vs best Euler vault for MON. Include current APRs and TVL.',
  maxSteps: 8,
})
console.log(`Model called ${steps.length} tools`)
console.log(text)""")

s.append(rule())
s.append(Spacer(1, 2*mm))

# ── 06 Aggregators ────────────────────────────────────────────────────────────
s += section_header('06   AGGREGATORS')

s.append(Paragraph('6.1  Multi-DEX Router', sH2))
s.append(Paragraph(
    'The router fans out to Kuru, Uniswap V3, PancakeSwap V3, PancakeSwap V2, Uniswap V2, '
    'and OpenOcean simultaneously via Promise.allSettled. It returns the route with the '
    'highest amountOut. Failed or timed-out sources are silently excluded from results.',
    sBody))
s += code_box("""const result = await getBestSwapRoute(MON, USDC, '1000000000000000000')
// result.bestDex   -> 'kuru'
// result.amountOut -> '354000'   (USDC, 6 decimals)
// result.allRoutes -> sorted by amountOut descending

const alert = await detectDexArbitrage(MON, USDC)
if (alert?.profitable) {
  console.log(`Spread: ${alert.spreadPct.toFixed(2)}%`)
}""")

s.append(Paragraph('6.2  Oracle Aggregator', sH2))
s.append(Paragraph(
    'getVerifiedPrice(symbol) queries Chainlink, Pyth, Redstone, Chronicle, and Kuru DEX, '
    'cross-validates results, and returns a confidence score. Confidence below 0.9 indicates '
    'significant inter-source deviation.',
    sBody))
s += tbl(
    ['Oracle', 'MON/USD', 'Notes'],
    [['Chainlink',  'N/A',         'No MON/USD feed on Monad. Individual feeds only.'],
     ['Pyth',       'Unconfirmed', 'Feed ID pending. May return incorrect value.'],
     ['Kuru DEX',   '$0.354',      'On-chain TWAP. Most reliable MON source.'],
     ['Redstone',   'Available',   'Pull-based. Prices embedded in calldata.'],
     ['Chronicle',  'Selected',    'Whitelisted system. Available for select assets.'],],
    [28*mm, 28*mm, 114*mm]
)

s.append(rule())
s.append(Spacer(1, 2*mm))

# ── 07 Technical Spec ─────────────────────────────────────────────────────────
s += section_header('07   TECHNICAL SPECIFICATIONS')

s.append(Paragraph('7.1  Stack', sH2))
s += tbl(
    ['Component', 'Technology', 'Details'],
    [['Language',    'TypeScript 5+',          'Strict mode; full declaration output'],
     ['Build',       'tsup',                   'ESM + CJS + DTS, tree-shakeable'],
     ['RPC Client',  'viem 2.x',               'publicClient pre-configured for Monad'],
     ['AI SDK',      'Vercel AI SDK v6',        'tool() with inputSchema: (Zod)'],
     ['Validation',  'Zod v4',                 'Runtime input validation for AI tools'],
     ['Oracle',      '@redstone-finance/sdk',  'Pull-based price data'],
     ['Testing',     'Vitest (singleFork)',     'Avoids 429 rate limit on public RPC'],
     ['Chain',       'Monad Mainnet',           'Chain ID 143, rpc.monad.xyz, 400ms blocks'],
     ['Multicall',   'Multicall3',              '0xcA11bde05977b3631167028862bE2a173976CA11'],],
    [30*mm, 42*mm, 98*mm]
)

s.append(Paragraph('7.2  Build Output', sH2))
s += tbl(
    ['File', 'Format', 'Size'],
    [['dist/index.js',    'ESM',        '224 KB'],
     ['dist/index.cjs',   'CommonJS',   '230 KB'],
     ['dist/index.d.ts',  'TypeScript', '396 KB'],
     ['dist/index.d.cts', 'TypeScript', '407 KB'],],
    [54*mm, 34*mm, 82*mm]
)

s.append(Paragraph('7.3  Monad RPC Notes', sH2))
for b in [
    'simulateContract required for Uniswap V3/V4 and Capricorn QuoterV2. readContract fails on non-view functions.',
    'Morpho vault discovery uses a bounded block range. eth_getLogs from block 0 is not supported.',
    'Euler V2 APR formula: interestRate() / 1e27 * 31_536_000. Stored as per-second ray value.',
    'watchEvent uses events: parameter (plural) in viem 2.x. Required for correct DTS with tsup.',
    'Vitest singleFork is mandatory. Parallel workers exhaust rate limits on the public RPC.',
    'BigInt serialization: API responses pass through safeJson() converting BigInt to string.',
]:
    s.append(Paragraph(f'  -  {b}', sBullet))

s.append(rule())
s.append(Spacer(1, 2*mm))

# ── 08 Token Registry ─────────────────────────────────────────────────────────
s += section_header('08   TOKEN REGISTRY')
s.append(Paragraph(
    'All addresses sourced from the official monad-crypto/token-list repository and verified '
    'against on-chain deployments. Checksummed EIP-55 format.',
    sBody))
s += tbl(
    ['Symbol', 'Decimals', 'Contract Address'],
    [['WMON',   '18', '0x3bd359C1119dA7Da1D913D1C4D2B7c461115433A'],
     ['USDC',   '6',  '0x754704Bc059F8C67012fEd69BC8A327a5aafb603'],
     ['AUSD',   '6',  '0x00000000eFE302BEAA2b3e6e1b18d08D69a9012a'],
     ['USDT0',  '6',  '0xe7cd86e13AC4309349F30B3435a9d337750fC82D'],
     ['WETH',   '18', '0xEE8c0E9f1BFFb4Eb878d8f15f368A02a35481242'],
     ['WBTC',   '8',  '0x0555E30da8f98308EdB960aa94C0Db47230d2B9c'],
     ['aprMON', '18', '0x0c65A0BC65a5D819235B71F554D210D3F80E0852'],
     ['sMON',   '18', '0xA3227C5969757783154C60bF0bC1944180ed81B9'],
     ['gMON',   '18', '0x8498312A6B3CbD158bf0c93AbdCF29E6e4F55081'],
     ['shMON',  '18', '0x1B68626dCa36c7fE922fD2d55E4f631d962dE19c'],],
    [22*mm, 20*mm, 128*mm]
)

s.append(rule())
s.append(Spacer(1, 2*mm))

# ── 09 Known Limitations ──────────────────────────────────────────────────────
s += section_header('09   KNOWN LIMITATIONS  &  ROADMAP')

s.append(Paragraph('v0.1.0 Limitations', sH2))
for b in [
    'nad.fun factory address is a placeholder. getNadFunTokens() returns empty until confirmed.',
    'Monday Markets reader (0x5678...placeholder) is unconfirmed. Function returns empty.',
    'Narwhal vault (0xabcd...placeholder) is unconfirmed.',
    'Pyth MON feed ID returns ~$1.00 (incorrect). getVerifiedPrice("MON") falls back to Kuru.',
    'Chainlink has no MON/USD feed. All Chainlink MON requests return null.',
]:
    s.append(Paragraph(f'  -  {b}', sBullet))

s.append(Paragraph('Planned Post-v0.1.0', sH2))
for b in [
    'Confirm and update placeholder contract addresses for nad.fun, Monday Markets, Narwhal.',
    'Verify Pyth MON feed ID and update oracle aggregator accordingly.',
    'Portfolio P&L tracking with historical block snapshots.',
    'WebSocket streaming endpoint for real-time swap events via Envio indexer.',
    'REST API server (rampart-api) for frontend and bot integrations.',
]:
    s.append(Paragraph(f'  -  {b}', sBullet))

s.append(rule())
s.append(Spacer(1, 2*mm))

# ── 10 Quick Start ────────────────────────────────────────────────────────────
s += section_header('10   QUICK START')
s.append(Paragraph('Install', sH3))
s += code_box("npm install rampart-monad")
s.append(Paragraph('Node.js 18+ and TypeScript 5+ required. ESM + CJS + DTS - no config needed.', sNote))
s.append(Paragraph('First call', sH3))
s += code_box("""import { getBestSwapRoute, getEulerVaults, getAllLSTStats } from 'rampart-monad'

const route  = await getBestSwapRoute(
  '0x0000000000000000000000000000000000000000',  // native MON
  '0x754704Bc059F8C67012fEd69BC8A327a5aafb603',  // USDC
  '1000000000000000000'
)
console.log(`Best: ${route.bestDex} -> ${route.amountOut}`)

const vaults = await getEulerVaults()
const lsts   = await getAllLSTStats()""")

s.append(Paragraph('Chain access', sH3))
s += code_box("""import { publicClient, monad, MONAD_CHAIN_ID } from 'rampart-monad'

const block = await publicClient.getBlockNumber()
console.log(monad.name)      // Monad Mainnet
console.log(MONAD_CHAIN_ID)  // 143""")

s.append(rule())
s.append(Spacer(1, 2*mm))

# ── 11 Links ──────────────────────────────────────────────────────────────────
s += section_header('11   LINKS  &  REFERENCES')
s += tbl(
    ['Resource', 'URL / Value'],
    [['npm package',          'https://www.npmjs.com/package/rampart-monad'],
     ['GitHub (SDK)',          'https://github.com/andrienkoj7crypto/rampart-monad'],
     ['Documentation',         'https://docs.rampartlabs.xyz'],
     ['Monad RPC',             'https://rpc.monad.xyz'],
     ['Token List (official)', 'https://github.com/monad-crypto/token-list'],
     ['Chain ID',              '143'],
     ['Multicall3',            '0xcA11bde05977b3631167028862bE2a173976CA11'],
     ['Book Manager (Clober)', '0x6657d192273731c3cac646cc82d5f28d0cbe8ccc'],],
    [48*mm, 122*mm]
)

s.append(Spacer(1, 8*mm))
s.append(Paragraph(
    'Rampart SDK v0.1.0   |   License: MIT   |   April 2026   |   rampartlabs.xyz',
    sFooter))

# ─── Render ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=16*mm, bottomMargin=16*mm,
    title='Rampart SDK - Technical Whitepaper v0.1.0',
    author='RampartLabs',
    subject='Unified DeFi SDK for Monad Mainnet',
)
doc.build(s, onFirstPage=page_cb, onLaterPages=page_cb)
print(f"Done: {OUT}")
