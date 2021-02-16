CREATE TABLE IF NOT EXISTS GITHUB_USERS(
               USERNAME CHAR(50) NOT NULL,
               ID INT,
               IMAGE_URL VARCHAR(150),
               TYPE CHAR(50),
               PROFILE_URL VARCHAR(150),
               UNIQUE(ID));

INSERT INTO GITHUB_USERS (USERNAME, ID, IMAGE_URL, TYPE, PROFILE_URL)
VALUES ("user1", 1, "https://images.google.l", "User", "https://github.com/profiles/user1");

INSERT INTO GITHUB_USERS (USERNAME, ID, IMAGE_URL, TYPE, PROFILE_URL)
VALUES ("user2", 2, "https://images.google.l", "User", "https://github.com/profiles/user2");

INSERT INTO GITHUB_USERS (USERNAME, ID, IMAGE_URL, TYPE, PROFILE_URL)
VALUES ("user3", 3, "https://images.google.l", "User", "https://github.com/profiles/user3");

INSERT INTO GITHUB_USERS (USERNAME, ID, IMAGE_URL, TYPE, PROFILE_URL)
VALUES ("user4", 4, "https://images.google.l", "User", "https://github.com/profiles/user4");

INSERT INTO GITHUB_USERS (USERNAME, ID, IMAGE_URL, TYPE, PROFILE_URL)
VALUES ("user5", 5, "https://images.google.l", "User", "https://github.com/profiles/user5");