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

### Option 1: Web UI (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt -r requirements-web.txt

# Start web server
python app.py

# Open browser: http://localhost:5000
```

**Modern, intuitive interface. No command line needed.**

### Option 2: Command Line

```bash
# Install dependencies
pip install -r requirements.txt

# Generate from example data
python cli.py generate --data data/example.yaml

# Output: output/acme-corporation-offer-2025-11-05.pptx
# Result: 632,961.00 EUR (calculated, formatted, ready to present)
```

**That's it.** Open the file. Present to client. Win the deal.

## Features

- 🌐 **Web UI** - Modern, intuitive interface (no command line needed)
- 📊 **Automatische Preisberechnung** - Stundensätze, Marge, Steuern, Rabatte
- 📈 **Dynamische Diagramme** - Timeline, Budget-Breakdown, Ressourcen-Allocation
- 🎨 **Professionelles Template** - 7 Folien, customizable, ready to present
- 💬 **Chat-Integration** - Daten aus Konversation extrahieren
- 📁 **File Upload** - Drag & drop YAML/JSON files
- 🚀 **Zero Friction** - Ein Befehl (oder ein Klick), ein Ergebnis
- ✅ **Type-Safe** - Pydantic validation, keine Laufzeitfehler
- 🧪 **Getestet** - Unit tests für alle Berechnungen

## All Commands

### Web UI
```bash
# Start web interface (recommended)
python app.py
# Open http://localhost:5000 in browser
```

### CLI Commands
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
- **WEB_UI.md** - Web interface guide (recommended)
- **USAGE.md** - Command-line usage guide with examples
- **SHOWCASE.md** - Deep dive into design philosophy and architecture

## The Vision

Technology married with elegance. Code that feels inevitable.

From conversation to professional presentation in minutes. Zero busywork. Maximum impact.

**Built with care. Designed with intention. Made to feel like magic.** ✨
