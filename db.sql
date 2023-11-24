CREATE DATABASE monitosnona;
USE monitosnona;

CREATE TABLE Cargo(
	id_cargo INT not null auto_increment,
	nombre VARCHAR(25) not null,
	PRIMARY KEY(id_cargo)
);

INSERT INTO cargo(nombre) VALUES('Vendedor');
INSERT INTO cargo(nombre) VALUES('Jefe de ventas');

CREATE TABLE Producto(
	id_producto INT not null auto_increment,
	nombre VARCHAR(50) not null,
	precio INT UNSIGNED not null,
	sku VARCHAR(20) not null,
	PRIMARY KEY(id_producto)
);

CREATE TABLE Usuario(
	id_usuario INT not null auto_increment,
	nombre_usuario VARCHAR(50) not null,
	nombre_completo VARCHAR(250),
	contra VARCHAR(20) not null,
	id_cargo INT,
	primary key(id_usuario),
	FOREIGN KEY (id_cargo) REFERENCES cargo(id_cargo)
);

CREATE TABLE Jornada(
	id_jornada INT not null auto_increment,
	estado BOOLEAN not null,
	fecha_inicio DATETIME,
	fecha_cierre DATETIME,
	PRIMARY KEY(id_jornada)
);

CREATE TABLE Factura(
	id_factura INT not null auto_increment,
	razon VARCHAR(50) not null,
	rut VARCHAR(12) not null
);

CREATE TABLE Venta(
	id_venta INT not null auto_increment,
	fecha DATETIME not null,
	id_usuario INT not null,
	id_jornada INT not null,
	id_factura INT,
	PRIMARY KEY(id_venta),
	FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
	FOREIGN KEY (id_jornada) REFERENCES jornadas(id_jornada),
	FOREIGN KEY (id_factura) REFERENCES facturas(id_factura)
);

CREATE TABLE Producto_venta(
	id_producto_venta INT not null auto_increment,
	id_producto INT not null,
	id_venta INT not null,
	PRIMARY KEY(id_producto_venta),
	FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
	FOREIGN KEY (id_venta) REFERENCES ventas(id_venta)
);
