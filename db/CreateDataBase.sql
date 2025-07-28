USE CarrosDB;

CREATE TABLE IF NOT EXISTS Carros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    ano INT NOT NULL
);

SET character_set_client = utf8;
SET character_set_connection = utf8;
SET character_set_results = utf8;
SET collation_connection = utf8_general_ci;

INSERT INTO Carros (marca, modelo, ano) VALUES
('Toyota', 'Corolla', 2020),
('Honda', 'Civic', 2019),
('Ford', 'Focus', 2018),
('Chevrolet', 'Onix', 2021),
('Volkswagen', 'Gol', 2022);
