PRAGMA foreign_keys = ON;
CREATE TABLE ActoLegal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    eurlex_ref TEXT,
    fecha DATE,
    texto_completo TEXT
);
CREATE TABLE Componente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    metadata TEXT
);
CREATE TABLE Acto_Componente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    acto_id INTEGER NOT NULL,
    componente_id INTEGER NOT NULL,
    disposicion TEXT,
    FOREIGN KEY (acto_id) REFERENCES ActoLegal(id),
    FOREIGN KEY (componente_id) REFERENCES Componente(id)
);
CREATE TABLE Keyword (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    componente_id INTEGER,
    keyword TEXT,
    FOREIGN KEY (componente_id) REFERENCES Componente(id)
);
