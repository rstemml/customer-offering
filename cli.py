#!/usr/bin/env python3
"""
Customer Offering Generator CLI

Philosophy: Simplicity is the ultimate sophistication.
"""

import click
import yaml
import json
import sys
from pathlib import Path
from datetime import date

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.models import Offer
from src.generator import generate_offer
from src.extractor import ChatExtractor
from src.calculator import PriceCalculator


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """
    🎨 Customer Offering Generator

    Transform conversations into professional PowerPoint offers.
    """
    pass


@cli.command()
@click.option('--data', '-d', type=click.Path(exists=True), required=True,
              help='Path to data file (YAML or JSON)')
@click.option('--template', '-t', type=click.Path(exists=True),
              default='templates/offer_template.pptx',
              help='Path to PowerPoint template')
@click.option('--output', '-o', type=click.Path(),
              help='Output path for generated offer')
def generate(data, template, output):
    """Generate offer from data file"""
    click.echo("🎨 Customer Offering Generator")
    click.echo("=" * 50)

    # Load data
    click.echo(f"📂 Loading data from {data}...")
    with open(data, 'r') as f:
        if data.endswith('.json'):
            offer_data = json.load(f)
        else:
            offer_data = yaml.safe_load(f)

    # Validate and create offer
    try:
        offer = Offer(**offer_data)
    except Exception as e:
        click.echo(f"❌ Error validating data: {e}", err=True)
        sys.exit(1)

    # Calculate pricing
    calculator = PriceCalculator(offer)
    breakdown = calculator.calculate_breakdown()

    click.echo(f"\n💰 Pricing Summary:")
    click.echo(f"   Customer: {offer.customer.name}")
    click.echo(f"   Project: {offer.project.name}")
    click.echo(f"   Duration: {offer.project.duration_months} months")
    click.echo(f"   Team: {calculator.get_team_size()} people")
    click.echo(f"   Total: {breakdown.format_currency(breakdown.total)}")

    # Generate output path if not specified
    if not output:
        customer_slug = offer.customer.name.lower().replace(' ', '-')
        output = f"output/{customer_slug}-offer-{date.today().isoformat()}.pptx"

    # Generate offer
    click.echo(f"\n✨ Generating offer...")
    try:
        result_path = generate_offer(offer, template, output)
        click.echo(f"\n🎉 Success!")
        click.echo(f"   {result_path}")
    except Exception as e:
        click.echo(f"❌ Error generating offer: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--template', '-t', type=click.Path(exists=True),
              default='templates/offer_template.pptx',
              help='Path to PowerPoint template')
@click.option('--output', '-o', type=click.Path(),
              help='Output path for generated offer')
def interactive(template, output):
    """Interactive mode - extract data from conversation"""
    click.echo("🎨 Customer Offering Generator - Interactive Mode")
    click.echo("=" * 50)
    click.echo("\nBeschreiben Sie das Angebot in natürlicher Sprache.")
    click.echo("Geben Sie Details zum Kunden, Projekt, Team und Preisen an.")
    click.echo("Drücken Sie Ctrl+D (Unix) oder Ctrl+Z (Windows) wenn fertig.\n")

    # Read multi-line input
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    conversation_text = '\n'.join(lines)

    if not conversation_text.strip():
        click.echo("❌ Keine Eingabe erhalten.", err=True)
        sys.exit(1)

    # Extract data
    click.echo("\n📝 Extrahiere Daten...")
    extractor = ChatExtractor()
    extracted_data = extractor.extract_from_text(conversation_text)

    # Show extracted data
    click.echo("\n✓ Extrahierte Daten:")
    click.echo("-" * 50)
    click.echo(extractor.to_yaml())
    click.echo("-" * 50)

    # Ask for confirmation
    if not click.confirm('\nDaten korrekt? Angebot generieren?'):
        click.echo("Abgebrochen.")
        sys.exit(0)

    # Create offer
    try:
        offer = Offer(**extracted_data)
    except Exception as e:
        click.echo(f"❌ Error validating data: {e}", err=True)
        click.echo("\nBitte passen Sie die Daten an und versuchen es erneut.")
        sys.exit(1)

    # Generate output path if not specified
    if not output:
        customer_slug = offer.customer.name.lower().replace(' ', '-')
        output = f"output/{customer_slug}-offer-{date.today().isoformat()}.pptx"

    # Generate offer
    click.echo(f"\n✨ Generating offer...")
    try:
        result_path = generate_offer(offer, template, output)
        click.echo(f"\n🎉 Success!")
        click.echo(f"   {result_path}")
    except Exception as e:
        click.echo(f"❌ Error generating offer: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('text', required=False)
@click.option('--file', '-f', type=click.Path(exists=True),
              help='Read text from file')
@click.option('--output', '-o', type=click.Path(),
              help='Save extracted data to file')
def extract(text, file, output):
    """Extract offer data from text"""
    click.echo("📝 Chat Extractor")
    click.echo("=" * 50)

    # Get input text
    if file:
        with open(file, 'r') as f:
            input_text = f.read()
    elif text:
        input_text = text
    else:
        click.echo("Geben Sie den Text ein (Ctrl+D zum Beenden):\n")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        input_text = '\n'.join(lines)

    if not input_text.strip():
        click.echo("❌ Keine Eingabe erhalten.", err=True)
        sys.exit(1)

    # Extract data
    extractor = ChatExtractor()
    extracted_data = extractor.extract_from_text(input_text)

    # Display result
    click.echo("\n✓ Extrahierte Daten:")
    click.echo(extractor.to_yaml())

    # Save if requested
    if output:
        with open(output, 'w') as f:
            if output.endswith('.json'):
                f.write(extractor.to_json())
            else:
                f.write(extractor.to_yaml())
        click.echo(f"\n💾 Gespeichert: {output}")


@cli.command()
@click.option('--data', '-d', type=click.Path(exists=True), required=True,
              help='Path to data file (YAML or JSON)')
def calculate(data):
    """Calculate pricing for an offer"""
    click.echo("💰 Price Calculator")
    click.echo("=" * 50)

    # Load data
    with open(data, 'r') as f:
        if data.endswith('.json'):
            offer_data = json.load(f)
        else:
            offer_data = yaml.safe_load(f)

    # Create offer
    try:
        offer = Offer(**offer_data)
    except Exception as e:
        click.echo(f"❌ Error validating data: {e}", err=True)
        sys.exit(1)

    # Calculate
    calculator = PriceCalculator(offer)
    breakdown = calculator.calculate_breakdown()

    # Display results
    click.echo(f"\nKunde: {offer.customer.name}")
    click.echo(f"Projekt: {offer.project.name}")
    click.echo(f"Dauer: {offer.project.duration_months} Monate\n")

    click.echo("Team Kosten:")
    for tc in breakdown.team_costs:
        click.echo(f"  {tc.role} ({tc.count}x): {breakdown.format_currency(tc.subtotal)}")

    click.echo(f"\nZwischensumme: {breakdown.format_currency(breakdown.subtotal)}")
    click.echo(f"Rabatt ({breakdown.discount_percent}%): -{breakdown.format_currency(breakdown.discount_amount)}")
    click.echo(f"Nach Rabatt: {breakdown.format_currency(breakdown.subtotal_after_discount)}")
    click.echo(f"MwSt. ({breakdown.tax_percent}%): +{breakdown.format_currency(breakdown.tax_amount)}")
    click.echo("\n" + "=" * 50)
    click.echo(f"GESAMT: {breakdown.format_currency(breakdown.total)}")


@cli.command()
@click.option('--output', '-o', type=click.Path(),
              default='templates/offer_template.pptx',
              help='Output path for template')
def init_template(output):
    """Create a new PowerPoint template"""
    click.echo("🎨 Template Builder")
    click.echo("=" * 50)

    from src.template_builder import TemplateBuilder

    builder = TemplateBuilder()
    builder.build_template(output)

    click.echo(f"\n✨ Template created successfully!")


if __name__ == '__main__':
    cli()
