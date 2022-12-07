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
        , image VARCHAR(20)
        , PRIMARY KEY(id_meuble)
);