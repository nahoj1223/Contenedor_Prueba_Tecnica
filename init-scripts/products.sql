CREATE TABLE products (
    sku VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    base_price INTEGER NOT NULL CHECK (base_price > 0),
    currency VARCHAR(10) NOT NULL,
    category VARCHAR(100) NOT NULL
);

INSERT INTO products (sku, name, base_price, currency, category) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'Morral Totto', 120000, 'COP', 'backpacks'),
('6f1e54b8-8326-4b4b-83f7-b2d3e4a20a98', 'Cuaderno Norma', 3, 'USD', 'stationery'),
('3c5f16d7-4e21-4ae7-babb-f3a8a3e6a2cc', 'Bolso Adidas', 180000, 'COP', 'bags'),
('f7d3e21a-89b0-4d5d-a1c8-24a5b72f71ee', 'Lonchera Escolar', 45000, 'COP', 'lunchboxes'),
('a2b4d72f-5e88-4e3b-9c88-0e8f9e4b0c7f', 'Canguro Nike', 50, 'USD', 'accessories');D