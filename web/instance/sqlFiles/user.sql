-- Create the User table
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,

    lastname TEXT,
    firstname TEXT,
    gender TEXT,
    budget REAL
);

