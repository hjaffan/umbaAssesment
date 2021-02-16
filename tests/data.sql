CREATE TABLE IF NOT EXISTS GITHUB_USERS(
               USERNAME CHAR(50) NOT NULL,
               ID INT,
               IMAGE_URL VARCHAR(150),
               TYPE CHAR(50),
               PROFILE_URL VARCHAR(150),
               UNIQUE(ID));