
-- $ sqlite3 drexelpedia.db < dev/db.sql

DROP TABLE IF EXISTS article;
CREATE TABLE article (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    votes INTEGER DEFAULT 0 NOT NULL
);

DROP TABLE IF EXISTS contributor;
CREATE TABLE contributor (
    id INTEGER PRIMARY KEY,
    submission_time INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    username TEXT NOT NULL
);

DROP TABLE IF EXISTS user;
CREATE TABLE user (
    username TEXT PRIMARY KEY,
    encrypted_password TEXT NOT NULL,
    reputation INTEGER DEFAULT 0 NOT NULL
);
