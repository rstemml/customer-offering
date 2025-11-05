# Customer Offering Generator

**Eleganz trifft Automatisierung.**

Ein System, das Kundenangebote aus Konversation generiert. Keine PowerPoint-Hölle. Nur Daten rein, Angebot raus.

> You speak. The system understands. Professional PowerPoint appears. **Zero friction.**

## What It Does

Transform conversations into professional PowerPoint offers with:
- 💰 Automatic price calculations (accurate to the cent)
- 📊 Dynamic charts (timeline, budget breakdown)
- 📋 Professional tables (team composition, pricing details)
- 🎨 Customizable templates (your branding, your colors)
- 💬 Natural language input (write like you talk)

**Example:** "Angebot für Acme Corp, 6 Monate, 3 Senior Developers à 800€/Tag, 10% Rabatt"
→ Professional 7-slide PowerPoint with calculations, charts, tables ✨

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Generate from example data
python cli.py generate --data data/example.yaml

# Output: output/acme-corporation-offer-2025-11-05.pptx
# Result: 632,961.00 EUR (calculated, formatted, ready to present)
```

**That's it.** Open the file. Present to client. Win the deal.

## Features

- 📊 **Automatische Preisberechnung** - Stundensätze, Marge, Steuern, Rabatte
- 📈 **Dynamische Diagramme** - Timeline, Budget-Breakdown, Ressourcen-Allocation
- 🎨 **Professionelles Template** - 7 Folien, customizable, ready to present
- 💬 **Chat-Integration** - Daten aus Konversation extrahieren
- 🚀 **Zero Friction** - Ein Befehl, ein Ergebnis
- ✅ **Type-Safe** - Pydantic validation, keine Laufzeitfehler
- 🧪 **Getestet** - Unit tests für alle Berechnungen

## All Commands

```bash
# Generate from YAML/JSON
python cli.py generate --data data/example.yaml

# Interactive mode
python cli.py interactive

# Extract data from text
python cli.py extract --file conversation.txt --output data/extracted.yaml

# Preview pricing
python cli.py calculate --data data/example.yaml

# Create custom template
python cli.py init-template --output templates/custom.pptx
```

## Architecture

```
customer-offering/
├── templates/          # PowerPoint templates
├── data/              # Customer data (YAML/JSON)
├── output/            # Generated offers
├── src/
│   ├── models.py      # Data models
│   ├── calculator.py  # Price calculation engine
│   ├── charts.py      # Chart generation
│   ├── generator.py   # Template filling engine
│   └── extractor.py   # Chat-to-data extraction
└── cli.py            # Command-line interface
```

## Documentation

- **README.md** (this file) - Overview and quick start
- **USAGE.md** - Detailed usage guide with examples
- **SHOWCASE.md** - Deep dive into design philosophy and architecture

## The Vision

Technology married with elegance. Code that feels inevitable.

From conversation to professional presentation in minutes. Zero busywork. Maximum impact.

**Built with care. Designed with intention. Made to feel like magic.** ✨
