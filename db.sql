CREATE DATABASE monitosnona;
USE monitosnona;

CREATE TABLE cargo (
	id_cargo INT not null auto_increment,
    nombre VARCHAR(25),
    PRIMARY KEY(id_cargo)
);

INSERT INTO cargo(nombre) VALUES('Vendedor');
INSERT INTO cargo(nombre) VALUES('Jefe de ventas');

CREATE TABLE productos (
	id_producto INT not null auto_increment,
    nombre VARCHAR(50),
    precio INT,
    sku VARCHAR(20),
    PRIMARY KEY(id_producto)
);

CREATE TABLE usuarios (
	id_usuario INT not null auto_increment,
	nombre_usuario VARCHAR(50),
    nombre_completo VARCHAR(250),
	contra VARCHAR(20) not null,
	id_cargo INT,
	primary key(id_usuario),
	FOREIGN KEY (id_cargo) REFERENCES cargo(id_cargo)
);

CREATE TABLE jornadas (
	id_jornada INT not null auto_increment,
    estado BOOLEAN,
    fecha_inicio DATETIME,
    fecha_cierre DATETIME,
    PRIMARY KEY(id_jornada)
);

CREATE TABLE ventas(
	id_venta INT not null auto_increment,
    fecha DATETIME,
    id_usuario INT,
    id_jornada INT,
    PRIMARY KEY(id_venta),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_jornada) REFERENCES jornadas(id_jornada)
);

CREATE TABLE carrito(
	id_carrito INT not null auto_increment,
    id_producto INT,
    id_venta INT,
    PRIMARY KEY(id_carrito),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta)
);
