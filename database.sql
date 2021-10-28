-- ENGINE = InnoDB

-- Tabla centros Medicos

CREATE TABLE centrosMedicos(
    IDcentroMedico INT(11) UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nombreCentroMedico VARCHAR(200) NOT NULL,
    numeroDeSerie VARCHAR(50) NOT NULL UNIQUE,
    codigoAcceso VARCHAR(50) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    imagenLogo LONGBLOB NULL,
    fechaUnion timestamp NOT NULL DEFAULT current_timestamp
);

-- Tabla de usuarios 
CREATE TABLE usuarios(
    IDuser INT(11) UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,
    vacunadoPor VARCHAR(200) NOT NULL,
    nombreUser VARCHAR(200) NOT NULL,
    tipoIdentificacion VARCHAR(50) NOT NULL,
    numeroIdentificacion VARCHAR(100) NOT NULL,
    imagenUser LONGBLOB NULL,
    tipoVacuna VARCHAR(25) NOT NULL,
    dosis VARCHAR(20) NOT NULL,
    fechaUnion timestamp NOT NULL DEFAULT current_timestamp,
    correo VARCHAR(300),
    CONSTRAINT fk_empresa FOREIGN KEY (vacunadoPor)
    REFERENCES centrosMedicos (numeroDeSerie)
);


