"""
Price Calculator - The math behind the offer.

Philosophy: Calculations should be transparent, accurate, and debuggable.
"""

from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass
from typing import List
from src.models import Offer, TeamMember


@dataclass
class TeamCost:
    """Cost breakdown for a team member role"""
    role: str
    count: int
    daily_rate: Decimal
    allocation_percent: int
    days_per_month: int
    months: int

    @property
    def total_days(self) -> Decimal:
        """Total working days for this role"""
        base_days = Decimal(self.days_per_month * self.months * self.count)
        return (base_days * Decimal(self.allocation_percent)) / Decimal(100)

    @property
    def subtotal(self) -> Decimal:
        """Subtotal cost for this role"""
        return self.daily_rate * self.total_days

    def to_dict(self):
        """Convert to dictionary for reporting"""
        return {
            'role': self.role,
            'count': self.count,
            'daily_rate': float(self.daily_rate),
            'allocation_percent': self.allocation_percent,
            'total_days': float(self.total_days),
            'subtotal': float(self.subtotal)
        }


@dataclass
class PriceBreakdown:
    """Complete price breakdown"""
    team_costs: List[TeamCost]
    subtotal: Decimal
    discount_percent: Decimal
    discount_amount: Decimal
    subtotal_after_discount: Decimal
    tax_percent: Decimal
    tax_amount: Decimal
    total: Decimal

    def to_dict(self):
        """Convert to dictionary for reporting"""
        return {
            'team_costs': [tc.to_dict() for tc in self.team_costs],
            'subtotal': float(self.subtotal),
            'discount_percent': float(self.discount_percent),
            'discount_amount': float(self.discount_amount),
            'subtotal_after_discount': float(self.subtotal_after_discount),
            'tax_percent': float(self.tax_percent),
            'tax_amount': float(self.tax_amount),
            'total': float(self.total)
        }

    def format_currency(self, amount: Decimal) -> str:
        """Format amount as EUR currency"""
        rounded = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return f"{rounded:,.2f} €".replace(',', ' ')


class PriceCalculator:
    """Calculates offer pricing"""

    def __init__(self, offer: Offer):
        self.offer = offer

    def calculate_team_costs(self) -> List[TeamCost]:
        """Calculate costs for each team member role"""
        costs = []

        for member in self.offer.team:
            cost = TeamCost(
                role=member.role,
                count=member.count,
                daily_rate=member.daily_rate,
                allocation_percent=member.allocation_percent,
                days_per_month=self.offer.pricing.working_days_per_month,
                months=self.offer.project.duration_months
            )
            costs.append(cost)

        return costs

    def calculate_breakdown(self) -> PriceBreakdown:
        """Calculate complete price breakdown"""
        # Calculate team costs
        team_costs = self.calculate_team_costs()

        # Subtotal
        subtotal = sum((tc.subtotal for tc in team_costs), Decimal(0))

        # Discount
        discount_percent = self.offer.pricing.discount_percent
        discount_amount = (subtotal * discount_percent / Decimal(100)).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        subtotal_after_discount = subtotal - discount_amount

        # Tax
        tax_percent = self.offer.pricing.tax_percent
        tax_amount = (subtotal_after_discount * tax_percent / Decimal(100)).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )

        # Total
        total = subtotal_after_discount + tax_amount

        return PriceBreakdown(
            team_costs=team_costs,
            subtotal=subtotal,
            discount_percent=discount_percent,
            discount_amount=discount_amount,
            subtotal_after_discount=subtotal_after_discount,
            tax_percent=tax_percent,
            tax_amount=tax_amount,
            total=total
        )

    def get_team_size(self) -> int:
        """Get total team size"""
        return sum(member.count for member in self.offer.team)

    def get_budget_by_role(self) -> dict:
        """Get budget distribution by role (for pie chart)"""
        team_costs = self.calculate_team_costs()
        total = sum((tc.subtotal for tc in team_costs), Decimal(0))

        distribution = {}
        for tc in team_costs:
            percentage = (tc.subtotal / total * 100) if total > 0 else 0
            distribution[tc.role] = {
                'amount': float(tc.subtotal),
                'percentage': float(percentage)
            }

        return distribution


def calculate_offer_price(offer: Offer) -> PriceBreakdown:
    """Convenience function to calculate offer price"""
    calculator = PriceCalculator(offer)
    return calculator.calculate_breakdown()


# Example usage for testing
if __name__ == "__main__":
    import yaml
    from src.models import Offer

    # Load example
    with open('data/example.yaml', 'r') as f:
        data = yaml.safe_load(f)

    offer = Offer(**data)
    calculator = PriceCalculator(offer)
    breakdown = calculator.calculate_breakdown()

    print("💰 Price Calculation")
    print("=" * 50)
    print(f"\nTeam Costs:")
    for tc in breakdown.team_costs:
        print(f"  {tc.role} ({tc.count}x): {breakdown.format_currency(tc.subtotal)}")

    print(f"\nSubtotal: {breakdown.format_currency(breakdown.subtotal)}")
    print(f"Discount ({breakdown.discount_percent}%): -{breakdown.format_currency(breakdown.discount_amount)}")
    print(f"After Discount: {breakdown.format_currency(breakdown.subtotal_after_discount)}")
    print(f"Tax ({breakdown.tax_percent}%): +{breakdown.format_currency(breakdown.tax_amount)}")
    print(f"\n{'=' * 50}")
    print(f"TOTAL: {breakdown.format_currency(breakdown.total)}")
