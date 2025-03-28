CREATE DATABASE EL_CLIENTE;

USE EL_CLIENTE;

CREATE TABLE Cliente (
    id INT PRIMARY KEY,        
    nombre VARCHAR(100) NOT NULL,   
    apellidos VARCHAR(100) NOT NULL,  
    ciudad VARCHAR(100)        
);

CREATE TABLE Sucursal (
    id INT PRIMARY KEY,           
    nombre VARCHAR(100) NOT NULL, 
    ciudad VARCHAR(100)           
);


CREATE TABLE Producto (
    id INT PRIMARY KEY,          
    nombre VARCHAR(100) NOT NULL,
    tipoProducto VARCHAR(100)    
);


CREATE TABLE Inscripcion (
    idProducto INT,               
    idCliente INT,               
    PRIMARY KEY (idProducto, idCliente), 
    FOREIGN KEY (idProducto) REFERENCES Producto(id), 
    FOREIGN KEY (idCliente) REFERENCES Cliente(id)    
);


CREATE TABLE Disponibilidad (
    idSucursal INT,               
    idProducto INT,              
    PRIMARY KEY (idSucursal, idProducto),  
    FOREIGN KEY (idSucursal) REFERENCES Sucursal(id),  
    FOREIGN KEY (idProducto) REFERENCES Producto(id)   
);


CREATE TABLE Visitan (
    idSucursal INT,               
    idCliente INT,                
    fechaVisita DATE NOT NULL,    
    PRIMARY KEY (idSucursal, idCliente),   
    FOREIGN KEY (idSucursal) REFERENCES Sucursal(id), 
    FOREIGN KEY (idCliente) REFERENCES Cliente(id)    
);

-- INSERCION DE DATOS

INSERT INTO Cliente (id, nombre, apellidos, ciudad) VALUES
(1, 'Juan', 'Pérez', 'Bogotá'),
(2, 'María', 'Gómez', 'Medellín'),
(3, 'Carlos', 'López', 'Cali'),
(4, 'Ana', 'Martínez', 'Barranquilla'),
(5, 'Luis', 'Rodríguez', 'Cartagena');



INSERT INTO Sucursal (id, nombre, ciudad) VALUES
(1, 'Sucursal Norte', 'Bogotá'),
(2, 'Sucursal Centro', 'Medellín'),
(3, 'Sucursal Sur', 'Cali'),
(4, 'Sucursal Este', 'Barranquilla'),
(5, 'Sucursal Oeste', 'Cartagena');


INSERT INTO Producto (id, nombre, tipoProducto) VALUES
(1, 'Cuenta Ahorros', 'Bancario'),
(2, 'Cuenta Corriente', 'Bancario'),
(3, 'Tarjeta Crédito', 'Financiero'),
(4, 'Crédito Hipotecario', 'Financiero'),
(5, 'Seguro de Vida', 'Seguro');


INSERT INTO Inscripcion (idProducto, idCliente) VALUES
(1, 1),  -- Juan Pérez inscrito en Cuenta Ahorros
(2, 1),  -- Juan Pérez inscrito en Cuenta Corriente
(3, 2),  -- María Gómez inscrita en Tarjeta Crédito
(4, 3),  -- Carlos López inscrito en Crédito Hipotecario
(5, 4),  -- Ana Martínez inscrita en Seguro de Vida
(1, 5);  -- Luis Rodríguez inscrito en Cuenta Ahorros


INSERT INTO Disponibilidad (idSucursal, idProducto) VALUES
(1, 1),  -- Cuenta Ahorros disponible en Sucursal Norte
(2, 1),  -- Cuenta Ahorros disponible en Sucursal Centro
(3, 2),  -- Cuenta Corriente disponible en Sucursal Sur
(4, 3),  -- Tarjeta Crédito disponible en Sucursal Este
(5, 4),  -- Crédito Hipotecario disponible en Sucursal Oeste
(5, 5);  -- Seguro de Vida disponible en Sucursal Oeste



INSERT INTO Visitan (idSucursal, idCliente, fechaVisita) VALUES
(1, 1, '2024-10-01'),  
(2, 2, '2024-09-15'), 
(3, 3, '2024-08-25'),  
(4, 4, '2024-07-10'),  
(5, 5, '2024-06-30'),  
(5, 1, '2024-10-05');  


INSERT INTO Cliente (id, nombre, apellidos, ciudad) VALUES
(6, 'Fernando', 'Salazar', 'Bogotá'),
(7, 'Laura', 'Quintero', 'Cali'),
(8, 'Andrea', 'Soto', 'Medellín'),
(9, 'Pedro', 'Ramírez', 'Barranquilla');


INSERT INTO Sucursal (id, nombre, ciudad) VALUES
(6, 'Sucursal Norte', 'Cali'),
(7, 'Sucursal Centro', 'Cartagena');


INSERT INTO Producto (id, nombre, tipoProducto) VALUES
(6, 'Seguro de Auto', 'Seguro'),
(7, 'Inversión a Plazo Fijo', 'Financiero');


INSERT INTO Inscripcion (idProducto, idCliente) VALUES
(6, 6),  
(1, 7),  
(7, 8),  
(2, 9);  


INSERT INTO Disponibilidad (idSucursal, idProducto) VALUES
(6, 6),  
(7, 7);  


INSERT INTO Visitan (idSucursal, idCliente, fechaVisita) VALUES
(6, 6, '2024-11-01'),  
(6, 7, '2024-10-15'),  
(7, 8, '2024-09-30'),  
(5, 9, '2024-07-25');  


INSERT INTO Cliente (id, nombre, apellidos, ciudad) VALUES
(30, 'Sebastián', 'Méndez', 'Bogotá'),
(31, 'Iván', 'Ruiz', 'Medellín'),
(32, 'Julia', 'Moreno', 'Cali'),
(33, 'Daniel', 'Hernández', 'Barranquilla'),
(34, 'Alejandra', 'Castro', 'Cartagena');


INSERT INTO Inscripcion (idProducto, idCliente) VALUES
(1, 30),  -- Sebastián Méndez inscrito en Cuenta Ahorros
(2, 31),  -- Iván Ruiz inscrito en Cuenta Corriente
(3, 32),  -- Julia Moreno inscrita en Tarjeta Crédito
(4, 33),  -- Daniel Hernández inscrito en Crédito Hipotecario
(5, 34);  -- Alejandra Castro inscrita en Seguro de Vida


INSERT INTO Disponibilidad (idSucursal, idProducto) VALUES
(2, 2), 
(3, 3), 
(4, 4),
(5, 5)  -- Seguro de Vida en Sucursal Oeste
ON DUPLICATE KEY UPDATE idProducto = VALUES(idProducto);


INSERT INTO Visitan (idSucursal, idCliente, fechaVisita) VALUES
(1, 30, '2024-12-01'),  -- Sebastián Méndez visitó Sucursal Norte
(2, 31, '2024-12-02'),  -- Iván Ruiz visitó Sucursal Centro
(3, 32, '2024-12-03'),  -- Julia Moreno visitó Sucursal Sur
(4, 33, '2024-12-04'),  -- Daniel Hernández visitó Sucursal Este
(5, 34, '2024-12-05');  -- Alejandra Castro visitó Sucursal Oeste





-- ----------------------------------------------------------- CONSULTAS-------------------------------------------------------------------------------------------------

-- consulta SQL solicitada debe encontrar los clientes que tienen productos inscritos disponibles solo en las sucursales que visitan.

SELECT DISTINCT c.nombre
FROM cliente c
JOIN inscripcion i ON c.id = i.idCliente
JOIN disponibilidad d ON i.idProducto = d.idProducto
JOIN visitan v ON c.id = v.idCliente AND d.idSucursal = v.idSucursal
WHERE NOT EXISTS (
    -- Busca productos inscritos disponibles en sucursales que el cliente no visita
    SELECT 1
    FROM inscripcion i2
    JOIN disponibilidad d2 ON i2.idProducto = d2.idProducto
    WHERE i2.idCliente = c.id
    AND NOT EXISTS (
        SELECT 1
        FROM visitan v2
        WHERE v2.idCliente = c.id
        AND v2.idSucursal = d2.idSucursal
    )
);

-- Consulta clientes que tienen inscrito algun producto disponible en las sucursales que visitan

SELECT DISTINCT c.nombre, c.apellidos
FROM Cliente c
JOIN Inscripcion i ON c.id = i.idCliente
JOIN Disponibilidad d ON i.idProducto = d.idProducto
JOIN Visitan v ON c.id = v.idCliente AND d.idSucursal = v.idSucursal
WHERE d.idSucursal = v.idSucursal;


-- Consulta para obtener el numero de clientes que han visitado cada sucursal

SELECT s.nombre AS sucursal, COUNT(v.idCliente) AS num_visitas
FROM Sucursal s
JOIN Visitan v ON s.id = v.idSucursal
GROUP BY s.nombre;


-- Consulta para obtener la catidad de productos inscritos por cada cliente
SELECT c.nombre, c.apellidos, COUNT(i.idProducto) AS num_productos_inscritos
FROM Cliente c
JOIN Inscripcion i ON c.id = i.idCliente
GROUP BY c.id, c.nombre, c.apellidos;


-- Consulta para listar los productos que estan disponibles en mas de una sucursal
SELECT p.nombre AS producto, COUNT(d.idSucursal) AS num_sucursales
FROM Producto p
JOIN Disponibilidad d ON p.id = d.idProducto
GROUP BY p.nombre
HAVING COUNT(d.idSucursal) > 1;

-- Consulta para obtener los clientes que han visitando una sucursal pero no estan inscritos en ningun producto
SELECT DISTINCT c.nombre, c.apellidos
FROM Cliente c
JOIN Visitan v ON c.id = v.idCliente
LEFT JOIN Inscripcion i ON c.id = i.idCliente
WHERE i.idCliente IS NULL;


-- Obtener el numero de inscripciones por tipo de producto
SELECT p.tipoProducto, COUNT(i.idProducto) AS num_inscripciones
FROM Producto p
JOIN Inscripcion i ON p.id = i.idProducto
GROUP BY p.tipoProducto;

-- Listar clientes que estan inscritos en productos de un tipo especifico, ejemplo="Bancario"

SELECT DISTINCT c.nombre, c.apellidos
FROM Cliente c
JOIN Inscripcion i ON c.id = i.idCliente
JOIN Producto p ON i.idProducto = p.id
WHERE p.tipoProducto = 'Bancario';
