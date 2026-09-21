CREATE TABLE ativos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    categoria VARCHAR(100),
    responsavel VARCHAR(255),
    setor VARCHAR(255),
    localizacao VARCHAR(255),
    vulnerabilidades JSON
);
