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
