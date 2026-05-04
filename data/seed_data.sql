INSERT INTO ActoLegal (titulo, eurlex_ref, fecha, texto_completo) VALUES
('Reglamento Ejemplo 1', 'EUR-LEX-1', '2019-06-01', ''),
('Directiva Ejemplo 2', 'EUR-LEX-2', '2020-12-15', ''),
('Reglamento Ejemplo 3', 'EUR-LEX-3', '2021-03-22', '');
INSERT INTO Componente (tipo, nombre, descripcion, metadata) VALUES
('PaginaInformacion','Página: Insolvencia transfronteriza','Página con información y formularios','{}'),
('ServicioDigital','Registro de Empresas','Servicio de inscripción','{}'),
('ServicioDigital','Intercambio de documentos','Intercambio seguro','{}'),
('CampoDeDatos','NIF/NumeroIdentificacion','Campo de identificación','{}'),
('ParteInteresada','AdministradorConcursal','Actor del procedimiento','{}'),
('PaginaInformacion','Guía: Procedimientos de registro','Guía explicativa','{}');
INSERT INTO Keyword (componente_id, keyword) VALUES
(1,'insolvencia transfronteriza'),
(1,'administrador concursal'),
(2,'registro de empresas'),
(3,'intercambio de documentos'),
(4,'numero identificacion'),
(5,'administrador concursal'),
(6,'registro de empresas');

