-- Create the 'users' table only if it does not already exist
CREATE TABLE IF NOT EXISTS users (
    -- 'id' is an integer that cannot be null, auto-increments, and serves as the primary key
    id INT NOT NULL AUTO_INCREMENT,
    
    -- 'email' is a string with a maximum length of 255 characters, cannot be null, and must be unique
    email VARCHAR(255) NOT NULL UNIQUE,
    
    -- 'name' is a string with a maximum length of 255 characters, it can be null
    name VARCHAR(255),
    
    -- Set 'id' as the primary key of the table
    PRIMARY KEY (id)
);
