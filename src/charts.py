"""
Chart Generator - Visual storytelling through data.

Philosophy: Charts should tell a story, not just display data.
"""

from pptx.chart.data import ChartData, CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Tuple
from decimal import Decimal

from src.models import Offer
from src.calculator import PriceCalculator


class ChartGenerator:
    """Generates charts for PowerPoint presentations"""

    # Color palette for charts
    CHART_COLORS = [
        RGBColor(0, 102, 204),     # Blue
        RGBColor(255, 153, 0),     # Orange
        RGBColor(102, 204, 0),     # Green
        RGBColor(204, 51, 51),     # Red
        RGBColor(153, 51, 204),    # Purple
        RGBColor(0, 153, 153),     # Teal
        RGBColor(255, 204, 0),     # Yellow
        RGBColor(153, 153, 153),   # Gray
    ]

    def __init__(self, offer: Offer):
        self.offer = offer
        self.calculator = PriceCalculator(offer)

    def create_timeline_chart(self, slide, left, top, width, height):
        """
        Create a timeline chart showing project phases.
        Uses a bar chart to show phases over time.
        """
        # Calculate project timeline
        start_date = self.offer.project.start_date
        duration_months = self.offer.project.duration_months

        # Create phases (simplified example)
        phases = self._generate_project_phases(duration_months)

        # Create chart data
        chart_data = ChartData()
        chart_data.categories = [phase['name'] for phase in phases]

        # Add series for timeline
        chart_data.add_series('Dauer (Monate)', [phase['duration'] for phase in phases])

        # Add chart to slide
        chart = slide.shapes.add_chart(
            XL_CHART_TYPE.BAR_CLUSTERED,
            left, top, width, height,
            chart_data
        ).chart

        # Styling
        chart.has_legend = False
        chart.chart_title.text_frame.text = "Projekt Phasen"
        chart.chart_title.text_frame.paragraphs[0].font.size = Pt(18)
        chart.chart_title.text_frame.paragraphs[0].font.bold = True

        # Color the bars
        series = chart.series[0]
        for idx, point in enumerate(series.points):
            fill = point.format.fill
            fill.solid()
            fill.fore_color.rgb = self.CHART_COLORS[idx % len(self.CHART_COLORS)]

        return chart

    def create_budget_pie_chart(self, slide, left, top, width, height):
        """
        Create a pie chart showing budget distribution by role.
        """
        # Get budget distribution
        budget_by_role = self.calculator.get_budget_by_role()

        # Create chart data
        chart_data = ChartData()
        chart_data.categories = list(budget_by_role.keys())

        # Add series
        values = [data['amount'] for data in budget_by_role.values()]
        chart_data.add_series('Budget', values)

        # Add chart to slide
        chart = slide.shapes.add_chart(
            XL_CHART_TYPE.PIE,
            left, top, width, height,
            chart_data
        ).chart

        # Styling
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.RIGHT
        chart.legend.include_in_layout = False

        chart.chart_title.text_frame.text = "Budget Verteilung nach Rolle"
        chart.chart_title.text_frame.paragraphs[0].font.size = Pt(18)
        chart.chart_title.text_frame.paragraphs[0].font.bold = True

        # Show data labels with percentages
        chart.plots[0].has_data_labels = True
        data_labels = chart.plots[0].data_labels
        data_labels.show_percentage = True
        data_labels.show_value = False

        # Color slices
        series = chart.series[0]
        for idx, point in enumerate(series.points):
            fill = point.format.fill
            fill.solid()
            fill.fore_color.rgb = self.CHART_COLORS[idx % len(self.CHART_COLORS)]

        return chart

    def create_resource_chart(self, slide, left, top, width, height):
        """
        Create a stacked bar chart showing resource allocation over time.
        """
        # Create chart data
        chart_data = ChartData()
        chart_data.categories = [f"Monat {i+1}" for i in range(self.offer.project.duration_months)]

        # Add series for each role
        for member in self.offer.team:
            # Constant allocation over time (could be made dynamic)
            allocation = [member.count] * self.offer.project.duration_months
            chart_data.add_series(member.role, allocation)

        # Add chart to slide
        chart = slide.shapes.add_chart(
            XL_CHART_TYPE.COLUMN_STACKED,
            left, top, width, height,
            chart_data
        ).chart

        # Styling
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False

        chart.chart_title.text_frame.text = "Ressourcen über Zeit"
        chart.chart_title.text_frame.paragraphs[0].font.size = Pt(18)
        chart.chart_title.text_frame.paragraphs[0].font.bold = True

        # Color series
        for idx, series in enumerate(chart.series):
            for point in series.points:
                fill = point.format.fill
                fill.solid()
                fill.fore_color.rgb = self.CHART_COLORS[idx % len(self.CHART_COLORS)]

        return chart

    def _generate_project_phases(self, duration_months: int) -> List[dict]:
        """
        Generate typical project phases based on duration.
        This is a simplified example - could be made configurable.
        """
        if duration_months <= 2:
            phases = [
                {'name': 'Planung & Design', 'duration': 0.5},
                {'name': 'Entwicklung', 'duration': 1.0},
                {'name': 'Testing & Deployment', 'duration': 0.5},
            ]
        elif duration_months <= 4:
            phases = [
                {'name': 'Planung & Design', 'duration': 1},
                {'name': 'Entwicklung', 'duration': 2},
                {'name': 'Testing', 'duration': 0.5},
                {'name': 'Deployment & Support', 'duration': 0.5},
            ]
        else:
            # Scale phases proportionally
            base = duration_months / 6
            phases = [
                {'name': 'Analyse & Design', 'duration': base * 1},
                {'name': 'Sprint 1-2', 'duration': base * 2},
                {'name': 'Sprint 3-4', 'duration': base * 2},
                {'name': 'Testing & QA', 'duration': base * 0.5},
                {'name': 'Deployment & Übergabe', 'duration': base * 0.5},
            ]

        return phases


class TableGenerator:
    """Generates tables for PowerPoint presentations"""

    def __init__(self, offer: Offer):
        self.offer = offer
        self.calculator = PriceCalculator(offer)

    def create_team_table(self, slide, left, top, width, height):
        """Create team composition table"""
        team_costs = self.calculator.calculate_team_costs()

        # Create table
        rows = len(team_costs) + 1  # +1 for header
        cols = 5
        table = slide.shapes.add_table(rows, cols, left, top, width, height).table

        # Set column widths
        table.columns[0].width = Inches(2.5)  # Role
        table.columns[1].width = Inches(1.0)  # Count
        table.columns[2].width = Inches(1.5)  # Daily Rate
        table.columns[3].width = Inches(1.5)  # Days
        table.columns[4].width = Inches(1.5)  # Subtotal

        # Header row
        headers = ['Rolle', 'Anzahl', 'Tagessatz', 'Tage', 'Summe']
        for col_idx, header in enumerate(headers):
            cell = table.cell(0, col_idx)
            cell.text = header
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(0, 102, 204)

            # Header text styling
            paragraph = cell.text_frame.paragraphs[0]
            paragraph.font.bold = True
            paragraph.font.size = Pt(12)
            paragraph.font.color.rgb = RGBColor(255, 255, 255)

        # Data rows
        for row_idx, tc in enumerate(team_costs, start=1):
            # Role
            table.cell(row_idx, 0).text = tc.role

            # Count
            table.cell(row_idx, 1).text = str(tc.count)

            # Daily Rate
            table.cell(row_idx, 2).text = f"{float(tc.daily_rate):,.0f} €"

            # Total Days
            table.cell(row_idx, 3).text = f"{float(tc.total_days):,.0f}"

            # Subtotal
            table.cell(row_idx, 4).text = f"{float(tc.subtotal):,.0f} €"

            # Style data cells
            for col_idx in range(cols):
                cell = table.cell(row_idx, col_idx)
                paragraph = cell.text_frame.paragraphs[0]
                paragraph.font.size = Pt(11)

        return table

    def create_pricing_table(self, slide, left, top, width, height):
        """Create pricing details table"""
        breakdown = self.calculator.calculate_breakdown()

        # Create table
        rows = 6  # Subtotal, Discount, After Discount, Tax, Total, blank
        cols = 2
        table = slide.shapes.add_table(rows, cols, left, top, width, height).table

        # Set column widths
        table.columns[0].width = Inches(3)
        table.columns[1].width = Inches(2.5)

        # Data
        data = [
            ('Zwischensumme', breakdown.format_currency(breakdown.subtotal)),
            (f'Rabatt ({breakdown.discount_percent}%)', f'-{breakdown.format_currency(breakdown.discount_amount)}'),
            ('Nach Rabatt', breakdown.format_currency(breakdown.subtotal_after_discount)),
            (f'MwSt. ({breakdown.tax_percent}%)', breakdown.format_currency(breakdown.tax_amount)),
            ('', ''),  # Blank row for separation
            ('GESAMT', breakdown.format_currency(breakdown.total)),
        ]

        for row_idx, (label, value) in enumerate(data):
            # Label
            cell_label = table.cell(row_idx, 0)
            cell_label.text = label

            # Value
            cell_value = table.cell(row_idx, 1)
            cell_value.text = value

            # Styling
            for col_idx in range(cols):
                cell = table.cell(row_idx, col_idx)
                paragraph = cell.text_frame.paragraphs[0]
                paragraph.font.size = Pt(14)

                # Special styling for total row
                if row_idx == 5:  # Total row
                    paragraph.font.bold = True
                    paragraph.font.size = Pt(18)
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(0, 102, 204)
                    paragraph.font.color.rgb = RGBColor(255, 255, 255)

        return table
