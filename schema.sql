DROP TABLE IF EXISTS users;

CREATE TABLE users (
   username TEXT NOT NULL,
   password TEXT,
   email TEXT NOT NULl,
   student_no TEXT,
   course_name TEXT,
   name TEXT,
   time datetime,
   photo VARBINARY
   );