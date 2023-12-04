CREATE TABLE utilisateurs
(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(128) NOT NULL,
    email VARCHAR(128) NOT NULL,
    password VARCHAR(128) NOT NULL
    
);

CREATE TABLE allergenes
(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(128) NOT NULL
);

CREATE TABLE ustensiles 
(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(128) NOT NULL
);

CREATE TABLE user_ustensile (
    user_id INTEGER NOT NULL,
    ustensile_nom VARCHAR(128) NOT NULL,
    FOREIGN KEY (ustensile_nom) REFERENCES ustensiles (nom) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES utilisateurs (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    PRIMARY KEY (user_id, ustensile_nom)
);

CREATE TABLE user_allergene (
    user_id INTEGER NOT NULL,
    allergene_nom VARCHAR(128) NOT NULL,
    FOREIGN KEY (allergene_nom) REFERENCES allergenes (nom) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES utilisateurs (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    PRIMARY KEY (user_id, allergene_nom)
);

CREATE TABLE recette (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nom  VARCHAR(128) NOT NULL,
    nb_like INTEGER NOT NULL,
    nb_dislike INTEGER NOT NULL
);

CREATE TABLE details_recette (
    id_recette INTEGER NOT NULL,
    ingredient VARCHAR(128) NOT NULL,
    quantite INTEGER NOT NULL,
    unite VARCHAR(10) NOT NULL,
    FOREIGN KEY (id_recette) REFERENCES recette (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    PRIMARY KEY (id_recette,ingredient)
);


INSERT INTO utilisateurs (username,email,password) VALUES ("admin","oui@test.com","1234");

INSERT INTO allergenes (nom) VALUES ("Lait"),("Gluten"),
("Soja"),("Oeuf"),("Arachide"),("Moutarde"),
("Poissons"),("Noix"),("Mollusques"),("Céleri"),
("Crustacés");

INSERT INTO ustensiles (nom) VALUES ("Four"),("Plaque"),
("Micro-onde"),("Blender"),("Marmitte"),("Panier vapeur")
,("Crêpière"),("Poêle"),("Casserole");

INSERT INTO recette (nom,nb_like,nb_dislike) VALUES ("crepe",0,0),("curry",0,0);

INSERT INTO details_recette (id_recette,ingredient,quantite,unite) VALUES (1,"lait",100,'ml'),(1,"farine",100,'g'),(1,"oeuf",2,'u'),
 (2,"riz",200,'g'),(2,"curry",10,'g'),(2,"poulet",100,'g');