"""
Tests for price calculator
"""

import sys
from pathlib import Path
from decimal import Decimal

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import Offer, Customer, Project, TeamMember, PricingConfig
from src.calculator import PriceCalculator
from datetime import date


def test_basic_calculation():
    """Test basic price calculation"""
    offer = Offer(
        customer=Customer(
            name="Test Corp",
            contact_person="John Doe",
            email="john@test.com"
        ),
        project=Project(
            name="Test Project",
            duration_months=1,
            start_date=date(2025, 12, 1)
        ),
        team=[
            TeamMember(role="Developer", count=1, daily_rate=1000, allocation_percent=100)
        ],
        deliverables=["Development"],
        pricing=PricingConfig(
            working_days_per_month=20,
            discount_percent=0,
            tax_percent=0
        )
    )

    calculator = PriceCalculator(offer)
    breakdown = calculator.calculate_breakdown()

    # 1 developer * 1000 EUR/day * 20 days * 1 month = 20,000 EUR
    assert breakdown.subtotal == Decimal("20000")
    assert breakdown.discount_amount == Decimal("0")
    assert breakdown.tax_amount == Decimal("0")
    assert breakdown.total == Decimal("20000")

    print("✓ Basic calculation test passed")


def test_with_discount():
    """Test calculation with discount"""
    offer = Offer(
        customer=Customer(
            name="Test Corp",
            contact_person="John Doe",
            email="john@test.com"
        ),
        project=Project(
            name="Test Project",
            duration_months=1,
            start_date=date(2025, 12, 1)
        ),
        team=[
            TeamMember(role="Developer", count=1, daily_rate=1000, allocation_percent=100)
        ],
        deliverables=["Development"],
        pricing=PricingConfig(
            working_days_per_month=20,
            discount_percent=10,
            tax_percent=0
        )
    )

    calculator = PriceCalculator(offer)
    breakdown = calculator.calculate_breakdown()

    assert breakdown.subtotal == Decimal("20000")
    assert breakdown.discount_amount == Decimal("2000")  # 10% of 20000
    assert breakdown.subtotal_after_discount == Decimal("18000")
    assert breakdown.total == Decimal("18000")

    print("✓ Discount calculation test passed")


def test_with_tax():
    """Test calculation with tax"""
    offer = Offer(
        customer=Customer(
            name="Test Corp",
            contact_person="John Doe",
            email="john@test.com"
        ),
        project=Project(
            name="Test Project",
            duration_months=1,
            start_date=date(2025, 12, 1)
        ),
        team=[
            TeamMember(role="Developer", count=1, daily_rate=1000, allocation_percent=100)
        ],
        deliverables=["Development"],
        pricing=PricingConfig(
            working_days_per_month=20,
            discount_percent=0,
            tax_percent=19
        )
    )

    calculator = PriceCalculator(offer)
    breakdown = calculator.calculate_breakdown()

    assert breakdown.subtotal == Decimal("20000")
    assert breakdown.tax_amount == Decimal("3800")  # 19% of 20000
    assert breakdown.total == Decimal("23800")

    print("✓ Tax calculation test passed")


def test_multiple_team_members():
    """Test calculation with multiple team members"""
    offer = Offer(
        customer=Customer(
            name="Test Corp",
            contact_person="John Doe",
            email="john@test.com"
        ),
        project=Project(
            name="Test Project",
            duration_months=2,
            start_date=date(2025, 12, 1)
        ),
        team=[
            TeamMember(role="Architect", count=1, daily_rate=1200, allocation_percent=100),
            TeamMember(role="Developer", count=2, daily_rate=800, allocation_percent=100)
        ],
        deliverables=["Development"],
        pricing=PricingConfig(
            working_days_per_month=20,
            discount_percent=0,
            tax_percent=0
        )
    )

    calculator = PriceCalculator(offer)
    breakdown = calculator.calculate_breakdown()

    # 1 * 1200 * 20 * 2 = 48,000
    # 2 * 800 * 20 * 2 = 64,000
    # Total = 112,000
    assert breakdown.subtotal == Decimal("112000")
    assert breakdown.total == Decimal("112000")

    print("✓ Multiple team members test passed")


def test_partial_allocation():
    """Test calculation with partial allocation"""
    offer = Offer(
        customer=Customer(
            name="Test Corp",
            contact_person="John Doe",
            email="john@test.com"
        ),
        project=Project(
            name="Test Project",
            duration_months=1,
            start_date=date(2025, 12, 1)
        ),
        team=[
            TeamMember(role="Developer", count=1, daily_rate=1000, allocation_percent=50)
        ],
        deliverables=["Development"],
        pricing=PricingConfig(
            working_days_per_month=20,
            discount_percent=0,
            tax_percent=0
        )
    )

    calculator = PriceCalculator(offer)
    breakdown = calculator.calculate_breakdown()

    # 1 * 1000 * 20 * 1 * 0.5 = 10,000
    assert breakdown.subtotal == Decimal("10000")
    assert breakdown.total == Decimal("10000")

    print("✓ Partial allocation test passed")


if __name__ == "__main__":
    test_basic_calculation()
    test_with_discount()
    test_with_tax()
    test_multiple_team_members()
    test_partial_allocation()

    print("\n🎉 All calculator tests passed!")
