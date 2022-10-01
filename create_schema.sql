CREATE TABLE Tweets (
  id INT PRIMARY KEY,
  author_id INT NOT NULL,
  created_at DATETIME,
  tweet_text nvarchar(300) NOT NULL,
  referenced_tweet INT,
  reference_type tinyint,
  answersTo INT,
  source tinyint
)
GO

CREATE TABLE Authors (
  ID INT PRIMARY KEY,
  name varchar(100),
  username varchar(50),
  creation_date DATETIME,

)
GO
/*ALTER DATA TYPES Due to limitations on size */
ALTER TABLE Tweets ALTER COLUMN id varchar(100)
GO
ALTER TABLE Tweets ALTER COLUMN author_id varchar(100)
GO
ALTER TABLE Tweets ALTER COLUMN referenced_tweet varchar(100)
GO
ALTER TABLE Tweets ALTER COLUMN answersTo varchar(100)
GO
ALTER TABLE Authors ALTER COLUMN ID varchar(100)
GO
ALTER TABLE Tweets ALTER COLUMNS tweet_text varchar(600)
GO

/*Adding columns to Tweets Table */
ALTER TABLE Tweets ADD has_media bit
ALTER TABLE Tweets ADD media_type tinyint


CREATE INDEX IX_Authors on Tweets (author_id,created_at, answersTo)
CREATE INDEX IX_Creation_date on Tweets(created_at, author_id, answersTo, referenced_tweet,reference_type)
