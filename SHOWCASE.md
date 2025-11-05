# Customer Offering Generator - Showcase

> **"Simplicity is the ultimate sophistication."** — Leonardo da Vinci

## The Problem

You hate PowerPoint. You hate context switching between data sources and slides. You just want to input your offer details and get a professional presentation. **Zero friction.**

## The Solution

A system that transforms **conversation into PowerPoint**. Data in → Offer out. Elegant. Automatic. Inevitable.

---

## ✨ What It Does

### 1. **Automatic Price Calculation**
- Team costs by role
- Configurable working days, discount, tax
- Accurate to the cent using Decimal arithmetic
- Transparent breakdown

**Example:**
```bash
$ python cli.py calculate --data data/example.yaml

Team Kosten:
  Solution Architect (1x): 144 000.00 €
  Senior Developer (3x): 288 000.00 €
  Junior Developer (2x): 120 000.00 €
  QA Engineer (1x): 39 000.00 €

GESAMT: 632 961.00 €
```

### 2. **Dynamic Charts & Tables**
- Timeline bar chart (project phases)
- Budget breakdown pie chart
- Team composition table
- Pricing detail table

All generated programmatically from your data.

### 3. **Professional Templates**
- 7-slide structure
- Cover, Executive Summary, Team, Timeline, Budget, Pricing, Next Steps
- Customizable colors, fonts, layouts
- Your logo, your branding

### 4. **Chat-to-Data Extraction**
- Write in natural language
- System extracts structured data
- Review and adjust before generation

**Example:**
```
Erstelle Angebot für BMW Digital Solutions
Projekt: Cloud Migration
8 Monate, Start 01.01.2026
2x Senior Developer, 900 €/Tag
Rabatt: 5%
```
→ Extracts customer, project, team, pricing automatically

### 5. **Multiple Workflows**

**From Data File:**
```bash
python cli.py generate --data data/example.yaml
```

**Interactive Mode:**
```bash
python cli.py interactive
# Paste your description, press Ctrl+D
```

**Extract Only:**
```bash
python cli.py extract --file conversation.txt --output data/extracted.yaml
# Edit the YAML, then generate
python cli.py generate --data data/extracted.yaml
```

---

## 🎨 The Architecture

```
customer-offering/
├── templates/          # PowerPoint templates
├── data/              # Customer data (YAML/JSON)
├── output/            # Generated offers
├── src/
│   ├── models.py      # Pydantic data models (validated, typed)
│   ├── calculator.py  # Price calculation engine
│   ├── charts.py      # Chart & table generation
│   ├── generator.py   # Template filling orchestrator
│   ├── extractor.py   # Chat-to-data extraction
│   └── template_builder.py  # Creates initial template
├── cli.py            # Command-line interface
└── tests/            # Unit tests
```

**Principles:**
- **Separation of concerns** - Each module has one job
- **Type safety** - Pydantic models validate all data
- **Testability** - Pure functions, no hidden state
- **Extensibility** - Easy to add new charts, slides, features

---

## 📊 Real Examples

### Example 1: Acme Corporation
**Input:** `data/example.yaml`
- 6-month e-commerce project
- 4 roles, 7 people
- 10% discount, 19% tax

**Output:** `output/acme-corporation-offer-2025-11-05.pptx`
- **Total: 632,961.00 €**

### Example 2: BMW Digital Solutions
**Input:** Extracted from conversation
- 8-month cloud migration
- 6 people (Architects, DevOps, QA)
- 5% discount

**Output:** `output/bmw-offer-final.pptx`
- **Total: 1,124,169.20 €**

---

## 🚀 Quick Start

```bash
# Install
pip install -r requirements.txt

# Generate from example
python cli.py generate --data data/example.yaml

# View pricing first
python cli.py calculate --data data/example.yaml

# Interactive mode
python cli.py interactive
```

---

## 🎯 Design Philosophy

### 1. **Think Different**
Not just "replace text in slides." Generate living presentations: charts, tables, calculations. Dynamic, not static.

### 2. **Obsess Over Details**
- Decimal arithmetic (no floating point errors)
- Proper date handling
- Currency formatting (space separator, proper rounding)
- Professional color palette
- Consistent typography

### 3. **Simplify Ruthlessly**
- One command: `generate`
- One format: YAML (or JSON)
- One template: Professional, extensible
- Zero configuration needed

### 4. **Craft, Don't Code**
```python
class PriceCalculator:
    """Calculates offer pricing"""

    def calculate_breakdown(self) -> PriceBreakdown:
        """Calculate complete price breakdown"""
        # Every function name sings
        # Every abstraction feels natural
        # Every edge case handled with grace
```

---

## 🛠 Technology Stack

- **Python 3.x** - Clear, readable, powerful
- **python-pptx** - PowerPoint manipulation
- **Pydantic** - Data validation
- **Click** - CLI framework
- **PyYAML** - Configuration format
- **Decimal** - Financial precision

**Why these choices?**
- Pure Python (no heavy dependencies)
- Cross-platform (Windows, Mac, Linux)
- Extensible (easy to add features)
- Maintainable (clean, typed code)

---

## 📈 What Makes This Special

### Not Just a Template Filler

**Other tools:**
```
Find {{name}} → Replace with "Acme"
```

**This system:**
```
Data → Calculations → Charts → Tables → Presentation
```

### Intelligent Extraction

**Pattern matching** for natural language:
- Recognizes roles, rates, dates
- Handles German and English
- Flexible input format

### Professional Output

- Charts with consistent colors
- Tables with proper formatting
- Currency displayed correctly
- Dates in local format
- Layout that breathes

### Testable & Reliable

```python
def test_basic_calculation():
    # 1 developer * 1000 EUR/day * 20 days * 1 month
    assert breakdown.total == Decimal("20000")
```

All calculations verified. No surprises.

---

## 🎓 Lessons Learned

### 1. **Placeholders Are Powerful**
Use `{{TEAM_TABLE}}` markers in template. Generator finds and replaces with real tables/charts.

### 2. **Pydantic Is Essential**
Validation at the boundary. If data passes validation, generation succeeds.

### 3. **Decimal > Float**
Financial calculations demand precision. `Decimal("19.00")` not `19.0`.

### 4. **Charts Need Love**
python-pptx creates charts, but styling makes them shine. Colors, legends, labels matter.

### 5. **CLI Ergonomics Matter**
Good help text, clear output, progress indicators. The tool should feel good to use.

---

## 🔮 Future Enhancements

### Phase 2
- [ ] LLM integration for smarter extraction (OpenAI/Claude API)
- [ ] Multiple template support (select by industry)
- [ ] PDF export (presentations + contracts)
- [ ] Email integration (send directly to customer)

### Phase 3
- [ ] Web UI (upload data, download PowerPoint)
- [ ] Database storage (offer history, versioning)
- [ ] Comparison view (version A vs B)
- [ ] Signature workflow (DocuSign integration)

### Phase 4
- [ ] CRM integration (Salesforce, HubSpot)
- [ ] Real-time collaboration (multiple users)
- [ ] Template marketplace (community templates)
- [ ] Analytics dashboard (offer success rate)

---

## 💡 Use Cases

### Software Agencies
Generate client proposals in minutes, not hours.

### Consulting Firms
Standardized offers with custom branding per client.

### Freelancers
Professional presentations that win projects.

### Sales Teams
Quick quotes with accurate pricing, every time.

---

## 📝 Sample Workflow

```bash
# Morning: Client calls with requirements
# You: Take notes in natural language

$ cat > client-notes.txt
Kunde: TechVision AG
Projekt: Mobile App Development
6 Monate
3 iOS Developer
2 Backend Developer
Start: März 2026
^D

# Extract data
$ python cli.py extract --file client-notes.txt --output data/techvision.yaml

# Review and adjust extracted data
$ vim data/techvision.yaml

# Calculate pricing
$ python cli.py calculate --data data/techvision.yaml
# Total: 456,000 EUR - looks good!

# Generate offer
$ python cli.py generate --data data/techvision.yaml

# Output: output/techvision-ag-offer-2025-11-05.pptx

# Afternoon: Send to client
# Client: Impressed by professionalism and speed
# Result: Win the deal 🎉
```

---

## 🏆 The Impact

**Before:**
- 2-3 hours per offer
- Copy-paste errors
- Calculation mistakes
- Inconsistent formatting
- Manual chart creation
- Frustration

**After:**
- 5-10 minutes per offer
- Zero copy-paste
- Accurate calculations
- Consistent branding
- Automatic charts
- **Confidence**

---

## 🎨 The Vision

> "Technology alone is not enough. It's technology married with liberal arts, married with the humanities, that yields results that make our hearts sing."

This tool isn't about replacing PowerPoint. It's about **removing friction** between your ideas and professional output.

It's about spending time on **what matters** (understanding client needs, designing solutions) instead of **busywork** (copying numbers, aligning charts).

It's about tools that **amplify your craft**, not constrain it.

---

**Built with care. Designed with intention. Made to feel inevitable.**

---

## 📞 Get Started

```bash
git clone <your-repo>
cd customer-offering
pip install -r requirements.txt
python cli.py generate --data data/example.yaml
```

**Questions? Issues? Ideas?**

See `README.md` for overview
See `USAGE.md` for detailed guide
See `tests/` for code examples

**Now go build something insanely great.** 🚀
