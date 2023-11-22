CREATE USER 'auth_home'@'localhost' IDENTIFIED BY 'WelcomeHome';
CREATE USER 'auth_home'@'127.0.0.1' IDENTIFIED BY 'WelcomeHome';

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_home'@'localhost';
GRANT ALL PRIVILEGES ON auth.* TO 'auth_home'@'127.0.0.1';

USE auth;

CREATE TABLE user (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUES ('objectdeveloper@gmail.com', 'HireMe88!');

  




