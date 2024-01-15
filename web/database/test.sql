CREATE TABLE utilisateurs
(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(128) NOT NULL,
    email VARCHAR(128) NOT NULL,
    password VARCHAR(128) NOT NULL
);

CREATE TABLE info_utilisateur
(
    id INTEGER NOT NULL PRIMARY KEY,
    budget INTEGER,
    forname VARCHAR(128),
    surname VARCHAR(128),
    tel VARCHAR(10),
    sexe VARCHAR(1),
    FOREIGN KEY (id) REFERENCES utilisateurs (id) ON DELETE RESTRICT ON UPDATE CASCADE
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

CREATE TABLE favori (
    id_recette INTEGER NOT NULL,
    id_user INTEGER NOT NULL,
    FOREIGN KEY (id_recette) REFERENCES recipes (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_user) REFERENCES utilisateurs (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    PRIMARY KEY (id_recette,id_user)
);

CREATE TABLE like_recette (
    id_recette INTEGER NOT NULL,
    id_user INTEGER NOT NULL,
    value_like INTEGER NOT NULL,
    FOREIGN KEY (id_recette) REFERENCES recipes (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_user) REFERENCES utilisateurs (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    PRIMARY KEY (id_recette,id_user)
);

CREATE TABLE recipes(id INTEGER PRIMARY KEY, title VARCHAR NOT NULL, servings INTEGER NOT NULL, servingsunit VARCHAR NOT NULL, imageURL VARCHAR NOT NULL);
CREATE TABLE categories(id INTEGER PRIMARY KEY, name VARCHAR UNIQUE NOT NULL);
CREATE TABLE category(recipeid INTEGER NOT NULL, categoryid INTEGER NOT NULL, PRIMARY KEY(recipeid, categoryid), FOREIGN KEY(recipeid) REFERENCES recipes(id), FOREIGN KEY(categoryid) REFERENCES categories(id));
CREATE TABLE ingredients(id INTEGER PRIMARY KEY, name VARCHAR UNIQUE NOT NULL);
CREATE TABLE ingredient(recipeid INTEGER NOT NULL, line INTEGER NOT NULL, amountint INTEGER NOT NULL, amountnum INTEGER NOT NULL, amountdenom INTEGER NOT NULL, 
amountfloat REAL NOT NULL, unit CHARACTER(2) NOT NULL, ingredientid INTEGER NOT NULL, PRIMARY KEY(recipeid, line), FOREIGN KEY(recipeid) REFERENCES recipes(id), 
FOREIGN KEY(ingredientid) REFERENCES ingredients(id));

CREATE TABLE instruction(recipeid INTEGER NOT NULL, line INTEGER NOT NULL, txt TEXT NOT NULL, PRIMARY KEY(recipeid, line), FOREIGN KEY(recipeid) REFERENCES recipes(id));
CREATE TABLE ingredientsection(recipeid INTEGER NOT NULL, line INTEGER NOT NULL, title VARCHAR(60) NOT NULL, PRIMARY KEY (recipeid, line), FOREIGN KEY(recipeid) REFERENCES recipes(id));
CREATE TABLE instructionsection(recipeid INTEGER NOT NULL, line INTEGER NOT NULL, title VARCHAR NOT NULL, PRIMARY KEY (recipeid, line), FOREIGN KEY(recipeid) REFERENCES recipes(id));
