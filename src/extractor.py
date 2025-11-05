"""
Chat Extractor - Transforms conversation into structured data.

Philosophy: The user speaks naturally, the system understands.
"""

import json
import re
from datetime import date, timedelta
from typing import Dict, Any, Optional
from decimal import Decimal


class ChatExtractor:
    """
    Extracts offer data from natural language conversation.

    This is a rule-based extractor that can be enhanced with LLM integration.
    """

    def __init__(self):
        self.extracted_data = {
            'customer': {},
            'project': {},
            'team': [],
            'deliverables': [],
            'pricing': {}
        }

    def extract_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extract offer data from text.

        Args:
            text: Natural language text describing the offer

        Returns:
            Dictionary with extracted offer data
        """
        text_lower = text.lower()

        # Extract customer information
        self._extract_customer(text, text_lower)

        # Extract project information
        self._extract_project(text, text_lower)

        # Extract team composition
        self._extract_team(text, text_lower)

        # Extract deliverables
        self._extract_deliverables(text, text_lower)

        # Extract pricing configuration
        self._extract_pricing(text, text_lower)

        return self.extracted_data

    def _extract_customer(self, text: str, text_lower: str):
        """Extract customer information"""
        # Customer name
        customer_patterns = [
            r'kunde[n]?\s*[:\-]?\s*([A-ZÄÖÜa-zäöü\s&\.]+?)(?:\n|,|\.|für)',
            r'für\s+([A-ZÄÖÜa-zäöü\s&\.]+?)(?:\n|,|\s+\d)',
            r'angebot für\s+([A-ZÄÖÜa-zäöü\s&\.]+?)(?:\n|,|\s+\d)',
            r'firma[:\-]?\s*([A-ZÄÖÜa-zäöü\s&\.]+?)(?:\n|,|\.)',
        ]

        for pattern in customer_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                self.extracted_data['customer']['name'] = match.group(1).strip()
                break

        # Contact person
        contact_patterns = [
            r'kontakt[person]*[:\-]?\s*([A-ZÄÖÜa-zäöü\s\.]+?)(?:\n|,|\.)',
            r'ansprechpartner[:\-]?\s*([A-ZÄÖÜa-zäöü\s\.]+?)(?:\n|,|\.)',
        ]

        for pattern in contact_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                self.extracted_data['customer']['contact_person'] = match.group(1).strip()
                break

        # Email
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_match = re.search(email_pattern, text)
        if email_match:
            self.extracted_data['customer']['email'] = email_match.group(0)

        # Set defaults if missing
        if 'name' not in self.extracted_data['customer']:
            self.extracted_data['customer']['name'] = "Kunde"
        if 'contact_person' not in self.extracted_data['customer']:
            self.extracted_data['customer']['contact_person'] = "N/A"
        if 'email' not in self.extracted_data['customer']:
            self.extracted_data['customer']['email'] = "kontakt@kunde.de"

    def _extract_project(self, text: str, text_lower: str):
        """Extract project information"""
        # Project name
        project_patterns = [
            r'projekt[:\-]?\s*([A-ZÄÖÜa-zäöü\s\-&\.]+?)(?:\n|,|\d+\s+monat)',
            r'(?:für|an)\s+(?:ein[em]*\s+)?([A-ZÄÖÜa-zäöü\s\-]+(?:platform|system|website|app|portal))',
        ]

        for pattern in project_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                self.extracted_data['project']['name'] = match.group(1).strip()
                break

        # Duration in months
        duration_patterns = [
            r'(\d+)\s*monat[e]*',
            r'dauer[:\-]?\s*(\d+)\s*monat',
            r'laufzeit[:\-]?\s*(\d+)\s*monat',
        ]

        for pattern in duration_patterns:
            match = re.search(pattern, text_lower)
            if match:
                self.extracted_data['project']['duration_months'] = int(match.group(1))
                break

        # Start date
        date_patterns = [
            r'start[:\-]?\s*(\d{4}-\d{2}-\d{2})',
            r'start[:\-]?\s*(\d{1,2})\.(\d{1,2})\.(\d{4})',
            r'ab\s+(\d{1,2})\.(\d{1,2})\.(\d{4})',
        ]

        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                if len(match.groups()) == 1:
                    # ISO format
                    self.extracted_data['project']['start_date'] = match.group(1)
                else:
                    # DD.MM.YYYY format
                    day, month, year = match.groups()
                    self.extracted_data['project']['start_date'] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                break

        # Defaults
        if 'name' not in self.extracted_data['project']:
            self.extracted_data['project']['name'] = "Software Entwicklungsprojekt"
        if 'duration_months' not in self.extracted_data['project']:
            self.extracted_data['project']['duration_months'] = 6
        if 'start_date' not in self.extracted_data['project']:
            # Default to 1 month from now
            start = date.today() + timedelta(days=30)
            self.extracted_data['project']['start_date'] = start.isoformat()

    def _extract_team(self, text: str, text_lower: str):
        """Extract team composition"""
        # Role patterns
        team_patterns = [
            # "3 Senior Developers" or "3x Senior Developer"
            r'(\d+)x?\s+(senior|junior|lead)?\s*(developer|entwickler|architect|architekt|designer|qa|tester|engineer)',
            # "Solution Architect: 1"
            r'(solution\s+architect|technical\s+lead|scrum\s+master|product\s+owner)[:\-]?\s*(\d+)',
        ]

        roles_found = []

        for pattern in team_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                groups = match.groups()

                if len(groups) == 3:
                    count = int(groups[0])
                    level = groups[1] if groups[1] else ""
                    role_type = groups[2]
                    role = f"{level} {role_type}".strip().title()
                else:
                    role = groups[0].title()
                    count = int(groups[1])

                roles_found.append({'role': role, 'count': count})

        # Rate patterns (per day)
        rate_patterns = [
            r'(\d+)\s*€?\s*/\s*tag',
            r'tagessatz[:\-]?\s*(\d+)',
            r'daily\s+rate[:\-]?\s*(\d+)',
        ]

        rates = []
        for pattern in rate_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                rates.append(int(match.group(1)))

        # Combine roles with rates (or use defaults)
        default_rates = {
            'architect': 1200,
            'architekt': 1200,
            'senior': 800,
            'lead': 900,
            'developer': 600,
            'entwickler': 600,
            'junior': 500,
            'qa': 650,
            'tester': 650,
            'designer': 700,
        }

        for i, role_info in enumerate(roles_found):
            rate = rates[i] if i < len(rates) else self._guess_rate(role_info['role'], default_rates)

            self.extracted_data['team'].append({
                'role': role_info['role'],
                'count': role_info['count'],
                'daily_rate': rate,
                'allocation_percent': 100
            })

        # Default team if nothing found
        if not self.extracted_data['team']:
            self.extracted_data['team'] = [
                {'role': 'Senior Developer', 'count': 2, 'daily_rate': 800, 'allocation_percent': 100}
            ]

    def _guess_rate(self, role: str, default_rates: dict) -> int:
        """Guess daily rate based on role"""
        role_lower = role.lower()
        for keyword, rate in default_rates.items():
            if keyword in role_lower:
                return rate
        return 600  # Default fallback

    def _extract_deliverables(self, text: str, text_lower: str):
        """Extract deliverables"""
        # Look for bullet points or lists
        deliverable_patterns = [
            r'[-•*]\s*([A-ZÄÖÜa-zäöü\s&\-\(\)]+?)(?:\n|$)',
            r'deliverables?[:\-]?\s*([A-ZÄÖÜa-zäöü\s,&\-\(\)]+?)(?:\n\n|\Z)',
            r'leistungen[:\-]?\s*([A-ZÄÖÜa-zäöü\s,&\-\(\)]+?)(?:\n\n|\Z)',
        ]

        for pattern in deliverable_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                deliverable = match.group(1).strip()
                if deliverable and len(deliverable) > 5:
                    self.extracted_data['deliverables'].append(deliverable)

        # Default deliverables
        if not self.extracted_data['deliverables']:
            self.extracted_data['deliverables'] = [
                "Konzeption & Design",
                "Implementierung",
                "Testing & QA",
                "Deployment & Dokumentation"
            ]

    def _extract_pricing(self, text: str, text_lower: str):
        """Extract pricing configuration"""
        # Discount
        discount_pattern = r'rabatt[:\-]?\s*(\d+)\s*%'
        discount_match = re.search(discount_pattern, text_lower)
        if discount_match:
            self.extracted_data['pricing']['discount_percent'] = int(discount_match.group(1))

        # Tax
        tax_pattern = r'(?:mwst|steuer|tax)[:\-]?\s*(\d+)\s*%'
        tax_match = re.search(tax_pattern, text_lower)
        if tax_match:
            self.extracted_data['pricing']['tax_percent'] = int(tax_match.group(1))

        # Working days
        days_pattern = r'(\d+)\s*arbeitstage\s*pro\s*monat'
        days_match = re.search(days_pattern, text_lower)
        if days_match:
            self.extracted_data['pricing']['working_days_per_month'] = int(days_match.group(1))

        # Defaults
        if 'discount_percent' not in self.extracted_data['pricing']:
            self.extracted_data['pricing']['discount_percent'] = 0
        if 'tax_percent' not in self.extracted_data['pricing']:
            self.extracted_data['pricing']['tax_percent'] = 19
        if 'working_days_per_month' not in self.extracted_data['pricing']:
            self.extracted_data['pricing']['working_days_per_month'] = 20

    def to_yaml(self) -> str:
        """Convert extracted data to YAML string"""
        import yaml
        return yaml.dump(self.extracted_data, default_flow_style=False, allow_unicode=True)

    def to_json(self) -> str:
        """Convert extracted data to JSON string"""
        return json.dumps(self.extracted_data, indent=2, ensure_ascii=False)


def extract_offer_from_chat(text: str) -> Dict[str, Any]:
    """
    Convenience function to extract offer data from chat text.

    Args:
        text: Natural language description of the offer

    Returns:
        Dictionary with extracted data
    """
    extractor = ChatExtractor()
    return extractor.extract_from_text(text)


# Example usage
if __name__ == "__main__":
    example_text = """
    Erstelle Angebot für TechStart GmbH
    Kontakt: Sarah Müller, sarah@techstart.de

    Projekt: E-Commerce Platform Modernisierung
    Dauer: 6 Monate
    Start: 01.12.2025

    Team:
    - 1x Solution Architect, 1200 €/Tag
    - 3x Senior Developer, 800 €/Tag
    - 2x Junior Developer, 500 €/Tag

    Deliverables:
    - Architektur & Design
    - Backend API Development
    - Frontend Implementation
    - Testing & QA
    - Deployment

    Rabatt: 10%
    20 Arbeitstage pro Monat
    """

    extractor = ChatExtractor()
    data = extractor.extract_from_text(example_text)

    print("📝 Extracted Data:")
    print("=" * 50)
    print(extractor.to_yaml())
