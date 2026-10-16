CREATE DATABASE IF NOT EXISTS gestion_transporte
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'akamaru'@'localhost'
    IDENTIFIED BY 'gestion_de_transporte_akamaru';

ALTER USER 'akamaru'@'localhost'
    IDENTIFIED BY 'gestion_de_transporte_akamaru';

GRANT ALL PRIVILEGES ON gestion_transporte.*
    TO 'akamaru'@'localhost';
FLUSH PRIVILEGES;
