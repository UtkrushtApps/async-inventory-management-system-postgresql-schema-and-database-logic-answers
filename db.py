import asyncpg
import os
from typing import List, Dict, Any, Optional

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost/inventory')

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self._pool: Optional[asyncpg.pool.Pool] = None

    async def connect(self):
        if not self._pool:
            self._pool = await asyncpg.create_pool(dsn=self.dsn)

    async def disconnect(self):
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def _get_category_id(self, category_name: str) -> int:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow("SELECT id FROM categories WHERE name = $1", category_name)
            if row:
                return row['id']
            row = await conn.fetchrow(
                "INSERT INTO categories(name) VALUES($1) RETURNING id", category_name
            )
            return row['id']

    async def add_product(self, name: str, category: str, quantity: int, price: float) -> Dict[str, Any]:
        cat_id = await self._get_category_id(category)
        async with self._pool.acquire() as conn:
            try:
                row = await conn.fetchrow(
                    """
                    INSERT INTO products (name, category_id, quantity, price)
                    VALUES ($1, $2, $3, $4)
                    RETURNING id, name, category_id, quantity, price, created_at
                    """,
                    name, cat_id, quantity, price
                )
            except asyncpg.exceptions.UniqueViolationError:
                raise ValueError("Product with the same name and category already exists.")
            prod = dict(row)
            # Get category name
            prod['category'] = category
            del prod['category_id']
            return prod

    async def list_products(self) -> List[Dict[str, Any]]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT p.id, p.name, c.name as category, p.quantity, p.price, p.created_at
                FROM products p
                JOIN categories c ON p.category_id = c.id
                ORDER BY p.created_at DESC, p.id DESC
                """
            )
            return [dict(row) for row in rows]

# Global database instance

db = Database(DATABASE_URL)
