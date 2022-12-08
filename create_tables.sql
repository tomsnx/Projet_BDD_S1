DROP TABLE IF EXISTS type_meuble;
DROP TABLE IF EXISTS meuble;

CREATE TABLE type_meuble (
        id_type_meuble INT AUTO_INCREMENT
        , libelle VARCHAR(20)
        , PRIMARY KEY(id_type_meuble)
);

CREATE TABLE meuble (
        id_meuble INT AUTO_INCREMENT
        , nom_meuble VARCHAR(20)
        , prix NUMERIC(5, 2)
        , dateFabrication DATE
        , couleur VARCHAR(10)
        , materiaux VARCHAR(10)
        , type_meuble_id INT
        , nb_stock INT
        , PRIMARY KEY(id_meuble)
        , CONSTRAINT meuble_type_fk FOREIGN KEY (type_meuble_id) REFERENCES type_meuble(id_type_meuble)
);

INSERT INTO type_meuble (id_type_meuble, libelle)
 VALUES
 (NULL, 'test'),
 (NULL, 'OUI'),
 (NULL, 'Libero'),
 (NULL, 'Savary');

INSERT INTO meuble (id_meuble, nom_meuble, prix, dateFabrication, couleur, materiaux, type_meuble_id, nb_stock)
 VALUES
 (NULL, 'monMeuble', 19, '2020-01-01', 'blanc', 'acier', 1, 18),
 (NULL, 'tonMeuble', 25, '2020-01-01', 'noir', 'carton', 3, 60),
 (NULL, 'sonMeuble', 30, '2020-01-01', 'bleu', 'carton', 2, 35),
 (NULL, 'sesMeubles', 30, '2020-01-01', 'jaune', 'carton', 4, 35);