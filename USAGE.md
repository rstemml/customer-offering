# Usage Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python cli.py --version
```

## Quick Start

### 1. Generate from Data File

The simplest way: You have a YAML or JSON file with offer data.

```bash
python cli.py generate --data data/example.yaml
```

Output: `output/acme-corporation-offer-2025-11-05.pptx`

### 2. Interactive Mode

Extract data from natural language conversation:

```bash
python cli.py interactive
```

Then paste your offer description:

```
Erstelle Angebot für TechStart GmbH
Kontakt: Sarah Müller, sarah@techstart.de

Projekt: E-Commerce Platform
Dauer: 6 Monate
Start: 01.12.2025

Team:
- 1x Solution Architect, 1200 €/Tag
- 3x Senior Developer, 800 €/Tag

Deliverables:
- Architecture & Design
- Backend Development
- Testing & Deployment
```

Press `Ctrl+D` (Unix) or `Ctrl+Z` (Windows) when done.

### 3. Extract Data Only

Want to extract and save data without generating the offer?

```bash
python cli.py extract --file conversation.txt --output data/extracted.yaml
```

Edit the extracted YAML file, then generate:

```bash
python cli.py generate --data data/extracted.yaml
```

### 4. Calculate Pricing

Preview pricing without generating PowerPoint:

```bash
python cli.py calculate --data data/example.yaml
```

Output:
```
💰 Price Calculator
==================================================

Kunde: Acme Corporation
Projekt: E-Commerce Platform Modernisierung
Dauer: 6 Monate

Team Kosten:
  Solution Architect (1x): 144 000.00 €
  Senior Developer (3x): 288 000.00 €
  Junior Developer (2x): 120 000.00 €
  QA Engineer (1x): 39 000.00 €

Zwischensumme: 591 000.00 €
Rabatt (10%): -59 100.00 €
Nach Rabatt: 531 900.00 €
MwSt. (19%): +101 061.00 €

==================================================
GESAMT: 632 961.00 €
```

## Data Format

### YAML Example

```yaml
customer:
  name: "Acme Corporation"
  contact_person: "Max Mustermann"
  email: "max@acme.com"
  address: "Hauptstraße 123, 10115 Berlin"  # optional

project:
  name: "E-Commerce Platform Modernisierung"
  description: "Vollständige Überarbeitung..."  # optional
  duration_months: 6
  start_date: "2025-12-01"

team:
  - role: "Solution Architect"
    count: 1
    daily_rate: 1200
    allocation_percent: 100  # optional, default 100

  - role: "Senior Developer"
    count: 3
    daily_rate: 800

deliverables:
  - "Architecture & Design"
  - "Backend Development"
  - "Testing & QA"

pricing:
  working_days_per_month: 20  # optional, default 20
  discount_percent: 10         # optional, default 0
  tax_percent: 19             # optional, default 19
```

## Commands Reference

### `generate`

Generate PowerPoint offer from data file.

```bash
python cli.py generate \
  --data data/example.yaml \
  --template templates/offer_template.pptx \
  --output output/my-offer.pptx
```

Options:
- `--data, -d`: Path to YAML/JSON data file (required)
- `--template, -t`: Path to PowerPoint template (default: `templates/offer_template.pptx`)
- `--output, -o`: Output path (default: auto-generated)

### `interactive`

Interactive mode with chat extraction.

```bash
python cli.py interactive \
  --template templates/offer_template.pptx \
  --output output/my-offer.pptx
```

Options:
- `--template, -t`: Path to PowerPoint template
- `--output, -o`: Output path

### `extract`

Extract offer data from natural language text.

```bash
# From file
python cli.py extract --file conversation.txt --output data/extracted.yaml

# From argument
python cli.py extract "Angebot für Acme Corp, 6 Monate, 3 Entwickler"

# Interactive (paste text, then Ctrl+D)
python cli.py extract
```

Options:
- `--file, -f`: Read text from file
- `--output, -o`: Save extracted data to file (YAML or JSON)

### `calculate`

Calculate and display pricing.

```bash
python cli.py calculate --data data/example.yaml
```

Options:
- `--data, -d`: Path to data file (required)

### `init-template`

Create a new PowerPoint template.

```bash
python cli.py init-template --output templates/my_template.pptx
```

Options:
- `--output, -o`: Output path (default: `templates/offer_template.pptx`)

## Template Customization

The default template includes 7 slides:

1. **Cover** - Project name, customer, date
2. **Executive Summary** - Overview and key facts
3. **Team Composition** - Table with roles and costs
4. **Timeline** - Bar chart with project phases
5. **Budget Breakdown** - Pie chart by role
6. **Pricing Details** - Calculation table
7. **Next Steps** - Contact and action items

### Customize the Template

1. Generate the default template:
   ```bash
   python cli.py init-template --output templates/custom.pptx
   ```

2. Open in PowerPoint and customize:
   - Change colors, fonts, layouts
   - Add your logo
   - Modify text placeholders

3. Keep these placeholders for dynamic content:
   - `{{project_name}}` - Project name
   - `{{customer_name}}` - Customer name
   - `{{offer_date}}` - Offer date
   - `{{TEAM_TABLE}}` - Team composition table
   - `{{TIMELINE_CHART}}` - Timeline chart
   - `{{BUDGET_CHART}}` - Budget pie chart
   - `{{PRICING_TABLE}}` - Pricing table

## Advanced Usage

### Custom Template per Client

```bash
# Create client-specific template
python cli.py init-template --output templates/bmw_template.pptx

# Use it for generation
python cli.py generate \
  --data data/bmw.yaml \
  --template templates/bmw_template.pptx
```

### Batch Processing

Generate multiple offers:

```bash
for file in data/*.yaml; do
  echo "Generating offer for $file..."
  python cli.py generate --data "$file"
done
```

### Integration with CI/CD

```bash
# In your CI/CD pipeline
python cli.py generate --data offer-data.yaml --output dist/offer.pptx

# Upload to storage or email
aws s3 cp dist/offer.pptx s3://offers/
```

## Tips & Best Practices

1. **Start with calculation** - Always run `calculate` first to verify pricing
2. **Review extracted data** - When using `extract`, always review the YAML before generating
3. **Keep templates in version control** - Track template changes with Git
4. **Use descriptive role names** - "Senior Backend Developer" is better than "Dev"
5. **Add project descriptions** - Helps make the Executive Summary more compelling
6. **Test with small duration first** - Start with 1-2 months to verify calculations

## Troubleshooting

### "Template not found"

Generate the default template:
```bash
python cli.py init-template
```

### "Invalid data format"

Validate your YAML syntax:
```bash
python -c "import yaml; yaml.safe_load(open('data/example.yaml'))"
```

### Extraction not accurate

The extractor uses pattern matching. For best results:
- Use clear formatting with line breaks
- Include units (€/Tag, Monate, etc.)
- Use standard date formats (DD.MM.YYYY or YYYY-MM-DD)

If extraction fails, manually create a YAML file using the example format.

## Examples

See the `data/` directory for example data files:
- `data/example.yaml` - Full featured example
- `data/bmw-extracted.yaml` - Enterprise project example

## Need Help?

```bash
python cli.py --help
python cli.py COMMAND --help
```
