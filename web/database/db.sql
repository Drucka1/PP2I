CREATE TABLE utilisateurs (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(128) UNIQUE NOT NULL,
    email VARCHAR(128) UNIQUE NOT NULL,
    password VARCHAR(64) NOT NULL
);

CREATE TABLE info_utilisateur (
    id INTEGER NOT NULL PRIMARY KEY,
    budget INTEGER,
    forname VARCHAR(128),
    surname VARCHAR(128),
    tel VARCHAR(10) UNIQUE,
    sexe VARCHAR(1),
    FOREIGN KEY (id) REFERENCES utilisateurs (id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE allergenes (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(128) NOT NULL
);

CREATE TABLE ustensiles (
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

CREATE TABLE favori (
    id_recette INTEGER NOT NULL,
    id_user INTEGER NOT NULL,
    FOREIGN KEY (id_recette) REFERENCES recipes (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_user) REFERENCES utilisateurs (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    PRIMARY KEY (id_recette,id_user)
);

INSERT INTO utilisateurs (username,email,password) VALUES ("admin","oui@test.com","03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4");

INSERT INTO allergenes (nom) VALUES ("Milk"),("Gluten"),('Wheat'),('Corn'),
("Soy"),("Egg"),("Peanut"),("Mustarde"),('Tomato'),('Potato'),('Oil'),('Meat'),
("Fish"),("Nut"),("Celery"),("Shellfish");

INSERT INTO ustensiles (nom) VALUES ('Cutting board'),('Vegetable peeler'),
('Grated'),('Kitchen scales'),('Measuring bowl'),('Mixing bowl'),('Colander'),
('Rolling pin'),('Mixer'),("Blender"),('Oven'),('Microwave'),('Frying pan'),
('Saucepans'),('Oven dish'),('Roasting pan'),('Hotplate'),('Spatula'),('Kitchen tongs'),
('Whisk'),('Ladle'),('Corkscrew'),('Bottle opener'),('Steam basket'),
('Crepe maker');
