"""Product data models."""

from typing import List, Optional, Tuple
from sqlalchemy import func, distinct, text, Select, Engine
from sqlmodel import Field, Session, SQLModel, select
from sqlalchemy_dremio.flight import DremioDialect_flight
from sqlalchemy.dialects import registry

from ..data import Pagination
from ..data.repository import DremioRepository


class CustomDremioDialect(DremioDialect_flight):
    """Custom Dremio dialect that implements import_dbapi."""

    supports_statement_cache = False

    @classmethod
    def import_dbapi(cls):
        """Import DBAPI module for Dremio."""
        return DremioDialect_flight.dbapi()


# Register our custom dialect
registry.register("dremio.flight", "production_control.products.models", "CustomDremioDialect")


class Product(SQLModel, table=True):
    """View model for products we make."""

    __tablename__ = "products"
    __table_args__ = {"schema": "Vines"}

    id: int = Field(
        primary_key=True,
        title="ID",
        sa_column_kwargs={"info": {"ui_hidden": True}},
    )
    name: str = Field(
        title="Naam",
        description="Naam van het product",
        sa_column_kwargs={"info": {"ui_sortable": True}},
    )
    product_group_id: int = Field(
        title="Productgroep ID",
        sa_column_kwargs={"info": {"ui_hidden": True}},
    )
    product_group_name: str = Field(
        title="Productgroep",
        description="Naam van de productgroep",
        sa_column_kwargs={"info": {"ui_sortable": True}},
    )


class ProductRepository(DremioRepository[Product]):
    """Read-only repository for product data access.

    Currently using Dremio Flight protocol which doesn't support parameterized queries.
    """

    # Fields to search when filtering products
    search_fields = ["name", "product_group_name"]

    def __init__(self, connection: Optional[Engine] = None):
        """Initialize repository with optional connection."""
        super().__init__(Product, connection)

    def _apply_default_sorting(self, query: Select) -> Select:
        """Apply default sorting to query."""
        return query.order_by(self.model.product_group_name, self.model.name)

    def get_all(self) -> List[Product]:
        """Get all products from the data source."""
        with Session(self.engine) as session:
            query = self._apply_sorting(select(Product), None, False)
            result = session.execute(query)
            return [row[0] for row in result]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get a product by its ID."""
        with Session(self.engine) as session:
            return session.exec(select(Product).where(text(f"id = {product_id}"))).first()

    def get_paginated(
        self,
        page: int = 1,
        items_per_page: int = 10,
        sort_by: Optional[str] = None,
        descending: bool = False,
        filter_text: Optional[str] = None,
        pagination: Optional[Pagination] = None,
    ) -> Tuple[List[Product], int]:
        """Get paginated products from the data source."""
        page, items_per_page, sort_by, descending = self._validate_pagination(
            page, items_per_page, sort_by, descending, pagination
        )

        with Session(self.engine) as session:
            # Create base queries
            base_query = select(Product)
            count_stmt = select(func.count(distinct(Product.id)))

            # Execute paginated query
            return self._execute_paginated_query(
                session,
                base_query,
                count_stmt,
                page,
                items_per_page,
                filter_text,
                self.search_fields,
                sort_by,
                descending,
            )
