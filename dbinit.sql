CREATE TABLE readings(
   id serial PRIMARY KEY,
   temperature NUMERIC NULL,
   pressure NUMERIC NULL,
   humidity VARCHAR (30) NOT NULL,
   lastupdate TIMESTAMP NOT NULL
   );
