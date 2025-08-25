CREATE TABLE countries (
    code CHAR(2) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    iva INTEGER NOT NULL CHECK (iva >= 0 AND iva <= 100)
);

INSERT INTO countries (name, code, iva) VALUES
('Colombia', 'CO', 19),
('España', 'ES', 20),
('Alemania', 'DE', 19),
('Francia', 'FR', 20),
('Brasil', 'BR', 17),
('México', 'MX', 16),
('Argentina', 'AR', 21),
('Chile', 'CL', 19),
('Reino Unido', 'GB', 20);