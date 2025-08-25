CREATE TABLE coupons (
    code VARCHAR(50) NOT NULL PRIMARY KEY,
    description TEXT,
    discount_percentage INTEGER NOT NULL CHECK (discount_percentage >= 0 AND discount_percentage <= 100),
    valid_from DATE NOT NULL,
    valid_to DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO coupons (code, description, discount_percentage, valid_from, valid_to, is_active) VALUES
('WELCOME10', '10% de descuento en tu primera compra', 10, '2025-08-01', '2025-12-31', TRUE),
('BACKTOSCHOOL', 'Descuento para regreso a clases', 15, '2024-07-01', '2024-09-30', FALSE),
('SUMMER25', 'Oferta de verano', 25, '2025-06-01', '2025-08-31', TRUE),
('BLACKFRIDAY', 'Black Friday especial', 40, '2025-11-28', '2025-11-28', TRUE);