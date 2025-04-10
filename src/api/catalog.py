from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Annotated
from sqlalchemy import text
from src.database import engine  # Import our database engine

router = APIRouter()

# Define a Pydantic model for each catalog item.
class CatalogItem(BaseModel):
    sku: Annotated[str, Field(pattern=r"^[a-zA-Z0-9_]{1,20}$")]
    name: str
    quantity: Annotated[int, Field(ge=1, le=10000)]
    price: Annotated[int, Field(ge=1, le=500)]
    potion_type: List[int] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="Must contain exactly 4 elements: [r, g, b, d]",
    )

@router.get("/catalog/", tags=["catalog"], response_model=List[CatalogItem])
def get_catalog() -> List[CatalogItem]:
    """
    Retrieves the catalog from the global_inventory table.
    Only returns a potion entry if its count is greater than 0.
    """
    catalog_items = []

    # Open a connection to the database using a transaction.
    with engine.begin() as connection:
        sql = text("""
            SELECT red_potions, green_potions, blue_potions,
                   red_ml, green_ml, blue_ml
            FROM global_inventory
            LIMIT 1
        """)
        result = connection.execute(sql)
        # Use .mappings() to get a dictionary-like row
        row = result.mappings().fetchone()

    
    # If there is no row, return an empty list.
    if row is None:
        return catalog_items

    # For each potion color, include an entry in the catalog if its count is greater than 0.
    if row["red_potions"] > 0:
        catalog_items.append(CatalogItem(
            sku=f"RED_POTION_{row['red_potions']}",
            name="Red Potion",
            quantity=row["red_potions"],
            price=50,              # Set a fixed price or adjust as needed.
            potion_type=[100, 0, 0, 0]  # Representation: pure red potion.
        ))
    if row["green_potions"] > 0:
        catalog_items.append(CatalogItem(
            sku=f"GREEN_POTION_{row['green_potions']}",
            name="Green Potion",
            quantity=row["green_potions"],
            price=50,
            potion_type=[0, 100, 0, 0]  # Representation: pure green potion.
        ))
    if row["blue_potions"] > 0:
        catalog_items.append(CatalogItem(
            sku=f"BLUE_POTION_{row['blue_potions']}",
            name="Blue Potion",
            quantity=row["blue_potions"],
            price=50,
            potion_type=[0, 0, 100, 0]  # Representation: pure blue potion.
        ))

    return catalog_items
