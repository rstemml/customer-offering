"""
Data Models - The essence of an offer.

Philosophy: Data should be self-documenting and validated.
"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal


class Customer(BaseModel):
    """Customer information"""
    name: str = Field(..., description="Company name")
    contact_person: str = Field(..., description="Contact person name")
    email: str = Field(..., description="Contact email")
    address: Optional[str] = Field(None, description="Company address")


class TeamMember(BaseModel):
    """Team member role and pricing"""
    role: str = Field(..., description="Role title (e.g., 'Senior Developer')")
    count: int = Field(..., ge=1, description="Number of people in this role")
    daily_rate: Decimal = Field(..., gt=0, description="Daily rate in EUR")
    allocation_percent: int = Field(100, ge=1, le=100, description="Allocation percentage")

    @field_validator('daily_rate', mode='before')
    @classmethod
    def convert_to_decimal(cls, v):
        return Decimal(str(v))


class Project(BaseModel):
    """Project details"""
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    duration_months: int = Field(..., ge=1, description="Project duration in months")
    start_date: date = Field(..., description="Expected start date")


class PricingConfig(BaseModel):
    """Pricing configuration"""
    working_days_per_month: int = Field(20, ge=1, le=31, description="Working days per month")
    discount_percent: Decimal = Field(Decimal("0"), ge=0, le=100, description="Discount percentage")
    tax_percent: Decimal = Field(Decimal("19"), ge=0, le=100, description="Tax percentage (VAT)")

    @field_validator('discount_percent', 'tax_percent', mode='before')
    @classmethod
    def convert_to_decimal(cls, v):
        return Decimal(str(v))


class Offer(BaseModel):
    """Complete customer offer"""
    customer: Customer
    project: Project
    team: List[TeamMember] = Field(..., min_length=1, description="Team composition")
    deliverables: List[str] = Field(..., min_length=1, description="Project deliverables")
    pricing: PricingConfig = Field(default_factory=PricingConfig)

    # Metadata
    offer_date: date = Field(default_factory=date.today, description="Offer creation date")
    valid_until_days: int = Field(30, ge=1, description="Offer validity in days")

    class Config:
        json_schema_extra = {
            "example": {
                "customer": {
                    "name": "Acme Corp",
                    "contact_person": "Max Mustermann",
                    "email": "max@acme.com"
                },
                "project": {
                    "name": "E-Commerce Platform Modernization",
                    "duration_months": 6,
                    "start_date": "2025-12-01"
                },
                "team": [
                    {"role": "Solution Architect", "count": 1, "daily_rate": 1200},
                    {"role": "Senior Developer", "count": 3, "daily_rate": 800},
                    {"role": "Junior Developer", "count": 2, "daily_rate": 500}
                ],
                "deliverables": [
                    "Architecture & Design",
                    "Backend API Development",
                    "Frontend Implementation",
                    "Testing & QA",
                    "Deployment & Documentation"
                ]
            }
        }
