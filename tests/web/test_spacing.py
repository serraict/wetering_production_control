"""Tests for spacing web interface."""

import asyncio
from datetime import date
from decimal import Decimal
from uuid import UUID
from unittest.mock import Mock, patch

from nicegui.testing import User
from nicegui import ui

from production_control.spacing.models import WijderzetRegistratie


async def test_spacing_page_shows_table(user: User) -> None:
    """Test that spacing page shows a table with spacing data."""
    with patch("production_control.web.pages.spacing.SpacingRepository") as mock_repo_class:
        # Given
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        test_date = date(2023, 1, 1)
        mock_repo.get_paginated.return_value = (
            [
                WijderzetRegistratie(
                    id=UUID("12345678-1234-5678-1234-567812345678"),
                    partij_code="TEST123",
                    product_naam="Test Plant",
                    productgroep_naam="Test Group",
                    datum_oppotten_real=test_date,
                    datum_uit_cel_real=test_date,
                    datum_wdz1_real=test_date,
                    datum_wdz2_real=test_date,
                    aantal_planten_gerealiseerd=100,
                    aantal_tafels_totaal=10,
                    aantal_tafels_na_wdz1=15,
                    aantal_tafels_na_wdz2=20,
                    aantal_tafels_oppotten_plan=Decimal("10.0"),
                    dichtheid_oppotten_plan=100,
                    dichtheid_wz1_plan=50,
                    dichtheid_wz2_plan=25.0,
                    wijderzet_registratie_fout=False,
                ),
                WijderzetRegistratie(
                    id=UUID("87654321-8765-4321-8765-432187654321"),
                    partij_code="TEST456",
                    product_naam="Other Plant",
                    productgroep_naam="Other Group",
                    datum_oppotten_real=test_date,
                    datum_uit_cel_real=test_date,
                    datum_wdz1_real=test_date,
                    datum_wdz2_real=test_date,
                    aantal_planten_gerealiseerd=200,
                    aantal_tafels_totaal=20,
                    aantal_tafels_na_wdz1=25,
                    aantal_tafels_na_wdz2=30,
                    aantal_tafels_oppotten_plan=Decimal("20.0"),
                    dichtheid_oppotten_plan=100,
                    dichtheid_wz1_plan=50,
                    dichtheid_wz2_plan=25.0,
                    wijderzet_registratie_fout=True,
                ),
            ],
            2,  # total count
        )

        # When
        await user.open("/spacing")
        await user.should_see("Wijderzetten Overzicht")  # Wait for page to load

        # Then
        table = user.find(ui.table).elements.pop()
        assert table.columns == [
            {
                "name": "partij_code",
                "label": "Partij",
                "field": "partij_code",
                "sortable": True,
            },
            {
                "name": "product_naam",
                "label": "Product",
                "field": "product_naam",
                "sortable": True,
            },
            {
                "name": "productgroep_naam",
                "label": "Productgroep",
                "field": "productgroep_naam",
                "sortable": True,
            },
            {
                "name": "datum_oppotten_real",
                "label": "Oppotdatum",
                "field": "datum_oppotten_real",
                "sortable": True,
            },
            {
                "name": "datum_uit_cel_real",
                "label": "Uit cel",
                "field": "datum_uit_cel_real",
                "sortable": True,
            },
            {
                "name": "datum_wdz1_real",
                "label": "Wijderzet 1",
                "field": "datum_wdz1_real",
                "sortable": True,
            },
            {
                "name": "datum_wdz2_real",
                "label": "Wijderzet 2",
                "field": "datum_wdz2_real",
                "sortable": True,
            },
            {
                "name": "aantal_planten_gerealiseerd",
                "label": "Planten",
                "field": "aantal_planten_gerealiseerd",
                "sortable": True,
            },
            {
                "name": "aantal_tafels_totaal",
                "label": "Tafels totaal",
                "field": "aantal_tafels_totaal",
                "sortable": True,
            },
            {
                "name": "aantal_tafels_na_wdz1",
                "label": "Tafels na WZ1",
                "field": "aantal_tafels_na_wdz1",
                "sortable": True,
            },
            {
                "name": "aantal_tafels_na_wdz2",
                "label": "Tafels na WZ2",
                "field": "aantal_tafels_na_wdz2",
                "sortable": True,
            },
            {
                "name": "aantal_tafels_oppotten_plan",
                "label": "Tafels plan",
                "field": "aantal_tafels_oppotten_plan",
                "sortable": True,
            },
            {
                "name": "dichtheid_oppotten_plan",
                "label": "Dichtheid oppotten",
                "field": "dichtheid_oppotten_plan",
                "sortable": True,
            },
            {
                "name": "dichtheid_wz1_plan",
                "label": "Dichtheid WZ1",
                "field": "dichtheid_wz1_plan",
                "sortable": True,
            },
            {
                "name": "dichtheid_wz2_plan",
                "label": "Dichtheid WZ2",
                "field": "dichtheid_wz2_plan",
                "sortable": True,
            },
            {
                "name": "wijderzet_registratie_fout",
                "label": "Fout",
                "field": "wijderzet_registratie_fout",
                "sortable": True,
            },
            {"name": "actions", "label": "Acties", "field": "actions"},
        ]
        assert table.rows == [
            {
                "id": UUID("12345678-1234-5678-1234-567812345678"),
                "partij_code": "TEST123",
                "product_naam": "Test Plant",
                "productgroep_naam": "Test Group",
                "datum_oppotten_real": test_date,
                "datum_uit_cel_real": test_date,
                "datum_wdz1_real": test_date,
                "datum_wdz2_real": test_date,
                "aantal_planten_gerealiseerd": 100,
                "aantal_tafels_totaal": 10,
                "aantal_tafels_na_wdz1": 15,
                "aantal_tafels_na_wdz2": 20,
                "aantal_tafels_oppotten_plan": Decimal("10.0"),
                "dichtheid_oppotten_plan": 100,
                "dichtheid_wz1_plan": 50,
                "dichtheid_wz2_plan": 25.0,
                "wijderzet_registratie_fout": False,
            },
            {
                "id": UUID("87654321-8765-4321-8765-432187654321"),
                "partij_code": "TEST456",
                "product_naam": "Other Plant",
                "productgroep_naam": "Other Group",
                "datum_oppotten_real": test_date,
                "datum_uit_cel_real": test_date,
                "datum_wdz1_real": test_date,
                "datum_wdz2_real": test_date,
                "aantal_planten_gerealiseerd": 200,
                "aantal_tafels_totaal": 20,
                "aantal_tafels_na_wdz1": 25,
                "aantal_tafels_na_wdz2": 30,
                "aantal_tafels_oppotten_plan": Decimal("20.0"),
                "dichtheid_oppotten_plan": 100,
                "dichtheid_wz1_plan": 50,
                "dichtheid_wz2_plan": 25.0,
                "wijderzet_registratie_fout": True,
            },
        ]


async def test_spacing_page_filtering_calls_repository(user: User) -> None:
    """Test that entering a filter value calls the repository with the filter text."""
    with patch("production_control.web.pages.spacing.SpacingRepository") as mock_repo_class:
        # Given
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        mock_repo.get_paginated.return_value = ([], 0)  # Empty initial result

        # An asyncio.Event to signal when the repository is called with filter
        done_event = asyncio.Event()

        def on_get_paginated(
            page=1, items_per_page=10, sort_by=None, descending=False, filter_text=""
        ):
            if filter_text == "TEST123":
                done_event.set()  # Set the event when desired call is made
            return [], 0

        mock_repo.get_paginated.side_effect = on_get_paginated

        # When
        await user.open("/spacing")
        search_box = user.find(marker="search", kind=ui.input)
        search_box.type("TEST123")
        search_box.trigger("change")

        # Await until the event is set, or timeout if necessary
        try:
            await asyncio.wait_for(done_event.wait(), timeout=2.0)
        except asyncio.TimeoutError:
            raise RuntimeError("Timeout while waiting for repository call.")

        # Then verify repository was called with filter
        mock_repo.get_paginated.assert_called_with(
            page=1, items_per_page=10, sort_by=None, descending=False, filter_text="TEST123"
        )