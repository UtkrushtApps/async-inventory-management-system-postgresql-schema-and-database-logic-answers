# Solution Steps

1. Create the PostgreSQL schema with two tables: 'categories' for product categories (id, name, unique) and 'products' for inventory items (id, name, category_id, quantity, price, created_at, with foreign key to categories and a unique constraint on (name, category_id)).

2. Implement 'db.py' to manage database access asynchronously using asyncpg. Initialize a connection pool, and define methods to add a product (mapping category names to ids, inserting category if not present, checking for duplicates), and to list products (joining with categories for display). Ensure all methods are non-blocking.

3. Create 'main.py' with FastAPI endpoints: POST /products (add product) and GET /products (list products). Use Pydantic models for data validation, and wire endpoints to the async database methods.

4. Wire FastAPI startup/shutdown events to connect/disconnect the database asynchronously.

5. Handle race conditions and uniqueness by catching UniqueViolationError in 'add_product'. Return the correct error response if a duplicate is attempted.

6. Ensure the 'created_at' field is auto-filled on insertion and included in responses.

7. Test adding and listing products, confirming API correctness and database constraint enforcement.

