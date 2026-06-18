SHOW DATABASES;

CREATE DATABASE googleplaystore_db;
USE googleplaystore_db;

SELECT @@SQL_SAFE_UPDATES;
SET sql_safe_updates = 0;

SET GLOBAL local_infile = 1;
SHOW VARIABLES LIKE 'secure_file_priv';

-- TABLE 1 STRUCTURE APPS

CREATE TABLE googleplaystore (
    App VARCHAR(255),
    Category VARCHAR(100),
    Rating VARCHAR(20),
    Reviews VARCHAR(50),
    Size VARCHAR(50),
    Installs VARCHAR(50),
    Type VARCHAR(20),
    Price VARCHAR(50),
    `Content Rating` VARCHAR(50),
    Genres VARCHAR(255),
    `Last Updated` VARCHAR(100),
    `Current Ver` VARCHAR(100),
    `Android Ver` VARCHAR(100)
);

-- TABLE 2 STRUCTURE - USER REVIEWS


CREATE TABLE googleplayreviews (
    App VARCHAR(255),
    Translated_Review TEXT,
    Sentiment VARCHAR(50),
    Sentiment_Polarity VARCHAR(50),
    Sentiment_Subjectivity VARCHAR(50)
);


LOAD DATA LOCAL INFILE
'S:/home/dataset/googleplaystore.csv'
INTO TABLE googleplaystore
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE
'S:/home/dataset/googleplaystore_user_reviews.csv'
INTO TABLE googleplayreviews
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT * from  googleplaystore;
SELECT * from  googleplayreviews;

SELECT COUNT(*) AS total_apps
FROM googleplaystore;

SELECT COUNT(*) AS total_reviews
FROM googleplayreviews;

SELECT * FROM googleplaystore LIMIT 5;
SELECT * FROM googleplayreviews LIMIT 5;

DESCRIBE googleplaystore;
DESCRIBE googleplayreviews;

-- Check Missing Values

SELECT COUNT(*) AS missing_rating FROM googleplaystore
WHERE Rating IS NULL OR Rating = '';      
-- Rating 0

SELECT COUNT(*) AS missing_category FROM googleplaystore
WHERE Category IS NULL OR Category = '';
-- category 0

SELECT COUNT(*) AS missing_type FROM googleplaystore
WHERE Type IS NULL OR Type = '';
-- type 0

SELECT COUNT(*) AS missing_content_rating FROM googleplaystore
WHERE `Content Rating` IS NULL OR `Content Rating` = '';
-- content rating 1
SELECT * FROM googleplaystore
WHERE `Content Rating` IS NULL OR `Content Rating` = '';
-- Life Made WI-Fi Touchscreen Photo Frame is having missing Content Rating
-- In category it is having 1.9 
-- Size is 1000+ its should be in M(MB) OR K(KB)
-- Install should be in number and its having as free
-- Type should be free or paid but its numeric
-- Price should be in number
-- By looking at this row its obvious that data columns have shifted towards left

-- so the best thing is to delete as total apps is 10841 and missing or corrupted data is 1
DELETE FROM googleplaystore WHERE Category = '1.9';

-- Checking for duplicate apps
SELECT App, COUNT(*) AS duplicate_count FROM googleplaystore
GROUP BY App HAVING COUNT(*) > 1 ORDER BY duplicate_count DESC;

SELECT COUNT(*) AS duplicate_apps
FROM (
    SELECT App
    FROM googleplaystore
    GROUP BY App
    HAVING COUNT(*) > 1
) d;

SELECT * FROM googleplaystore WHERE App = 'ROBLOX';
-- 9 roblox rows categories are game and family but reviews aint the same

-- so the better way is for the same app most of the reviews can be different so based on reviews selected one with highest 
WITH ranked_apps AS (
    SELECT *,
           ROW_NUMBER() OVER(
               PARTITION BY App
               ORDER BY CAST(Reviews AS UNSIGNED) DESC
           ) AS rn
    FROM googleplaystore
)
SELECT * FROM ranked_apps WHERE rn = 1;

-- since we will be using for analysis creating a cleaned table will be good
CREATE TABLE googleplaystore_clean AS
WITH ranked_apps AS (
    SELECT *,
           ROW_NUMBER() OVER(
               PARTITION BY App
               ORDER BY CAST(Reviews AS UNSIGNED) DESC
           ) AS rn
    FROM googleplaystore
)
SELECT *
FROM ranked_apps
WHERE rn = 1;

SELECT * FROM googleplaystore_clean WHERE App = 'ROBLOX';
-- so duplicates removed

SELECT DISTINCT Installs FROM googleplaystore_clean ORDER BY Installs LIMIT 20;
SELECT Installs,
       REPLACE(REPLACE(Installs, ',', ''), '+', '') AS installs_clean
FROM googleplaystore_clean LIMIT 20;

UPDATE googleplaystore_clean
SET Installs = REPLACE(REPLACE(Installs, ',', ''), '+', '');

SELECT * from googleplaystore_clean;

SELECT DISTINCT Size from googleplaystore_clean;
SELECT COUNT(*) AS varies_count FROM googleplaystore_clean
WHERE Size = 'Varies with device';

ALTER TABLE googleplaystore_clean
ADD COLUMN Size_MB DECIMAL(10,3);

UPDATE googleplaystore_clean SET Size_MB =
CASE
    WHEN Size LIKE '%M'
        THEN CAST(REPLACE(Size,'M','') AS DECIMAL(10,3))

    WHEN Size LIKE '%k'
        THEN CAST(REPLACE(Size,'k','') AS DECIMAL(10,3)) / 1000

    WHEN Size = 'Varies with device'
        THEN NULL

    ELSE NULL
END;

SELECT * FROM googleplaystore_clean LIMIT 30;
-- Size column is cleaned and new cleaned column is Size_MB

SELECT DISTINCT Price FROM googleplaystore_clean ORDER BY Price;
-- so some are free and some are paid
ALTER TABLE googleplaystore_clean ADD COLUMN Price_Clean DECIMAL(10,2);

UPDATE googleplaystore_clean SET Price_Clean = CAST(REPLACE(Price, '$', '') AS DECIMAL(10,2));

SELECT Price, Price_Clean FROM googleplaystore_clean LIMIT 20;
SELECT * FROM googleplaystore_clean WHERE Price_Clean IS NULL;
-- there is no null in Price column


-- Data Quality Check
SELECT
    COUNT(*) AS total_rows,
    SUM(Rating IS NULL OR Rating = '') AS missing_rating,
    SUM(Size_MB IS NULL) AS missing_size,
    SUM(Price_Clean IS NULL) AS missing_price
FROM googleplaystore_clean;

-- Top Categories by Number of Apps
SELECT
    Category,
    COUNT(*) AS total_apps
FROM googleplaystore_clean
GROUP BY Category ORDER BY total_apps DESC;

-- Top Categories by Total Installs
SELECT
    Category,
    SUM(Installs) AS total_installs
FROM googleplaystore_clean
GROUP BY Category ORDER BY total_installs DESC;

-- GAME	13457414415 installs and leading


-- Free vs Paid Apps
SELECT
    Type,
    COUNT(*) AS total_apps,
    ROUND(AVG(Rating),2) AS avg_rating,
    ROUND(AVG(Installs),0) AS avg_installs
FROM googleplaystore_clean GROUP BY Type;

-- Free	8885	3.55	8459519
-- Paid	751	  3.41	76363
-- free are leading by total , avgrating and avginstalls

-- Rating Distribution
SELECT
    Rating,
    COUNT(*) AS app_count
FROM googleplaystore_clean WHERE Rating IS NOT NULL
GROUP BY Rating ORDER BY Rating DESC;

-- Content Rating Analysis
SELECT
    `Content Rating`,
    COUNT(*) AS total_apps,
    ROUND(AVG(Rating),2) AS avg_rating
FROM googleplaystore_clean GROUP BY `Content Rating`
ORDER BY total_apps DESC;

-- for everyone apps are highest with 7882 and avg rating 3.5

-- Top Rated Categories
SELECT
    Category,
    ROUND(AVG(Rating),2) AS avg_rating,
    COUNT(*) AS total_apps
FROM googleplaystore_clean WHERE Rating IS NOT NULL
GROUP BY Category HAVING COUNT(*) >= 50 ORDER BY avg_rating DESC;

-- education is highly rated 4.31 as average and total apps 106

-- Price vs Rating
SELECT
    ROUND(Price_Clean,0) AS price_bracket,
    ROUND(AVG(Rating),2) AS avg_rating,
    COUNT(*) AS apps
FROM googleplaystore_clean WHERE Price_Clean > 0
GROUP BY price_bracket ORDER BY price_bracket;


-- Top Apps by Reviews
SELECT App, Category, Reviews, Rating
FROM googleplaystore_clean ORDER BY Reviews DESC LIMIT 10;

-- MegaFon Dashboard	COMMUNICATION	99559	3.7

-- Sentiment Analysis
SELECT
    g.Category,
    ROUND(AVG(CAST(r.Sentiment_Polarity AS DECIMAL(10,4))),4) AS avg_sentiment,
    COUNT(*) AS review_count
FROM googleplaystore_clean g JOIN googleplayreviews r ON g.App = r.App
GROUP BY g.Category ORDER BY avg_sentiment DESC;

-- GAME	0.0407	9660
-- FAMILY	0.0726	5827


-- Top 3 Apps Within Each Category

WITH ranked_apps AS (
    SELECT Category, App, Reviews, Rating,
        DENSE_RANK() OVER (
            PARTITION BY Category
            ORDER BY CAST(Reviews AS UNSIGNED) DESC
        ) AS category_rank FROM googleplaystore_clean
)
SELECT Category, App, Reviews, Rating, category_rank
FROM ranked_apps WHERE category_rank <= 3 ORDER BY Category, category_rank;

-- ART_AND_DESIGN	Textgram - write on photos	295237	4.4	1
-- ART_AND_DESIGN	ibis Paint X	224399	4.6	2
-- ART_AND_DESIGN	Sketch - Draw & Paint	215644	4.5	3


-- Categories Performing Above Overall Average
WITH category_metrics AS (
    SELECT Category, AVG(Rating) AS avg_rating, AVG(Installs) AS avg_installs
    FROM googleplaystore_clean GROUP BY Category
),

overall_metrics AS (
    SELECT AVG(Rating) AS overall_rating, AVG(Installs) AS overall_installs
    FROM googleplaystore_clean
)
SELECT
    c.Category,
    ROUND(c.avg_rating,2) AS avg_rating,
    ROUND(c.avg_installs,0) AS avg_installs
FROM category_metrics c CROSS JOIN overall_metrics o
WHERE c.avg_rating > o.overall_rating AND c.avg_installs > o.overall_installs
ORDER BY c.avg_installs DESC;

-- VIDEO_PLAYERS	3.67	23975017
-- SOCIAL	3.6	23058247
-- PHOTOGRAPHY	3.89	16695332
-- GAME	4.03	14255736
-- ENTERTAINMENT	4.13	11449535


-- App Update Trend by Year Date Analysis

-- first cleaning and making a new column 
ALTER TABLE googleplaystore_clean
ADD COLUMN Last_Updated_Date DATE;

UPDATE googleplaystore_clean
SET Last_Updated_Date = STR_TO_DATE(`Last Updated`, '%M %d, %Y');

SELECT YEAR(Last_Updated_Date) AS update_year, COUNT(*) AS apps_updated
FROM googleplaystore_clean GROUP BY update_year ORDER BY update_year;

-- 2018	6272
-- 2017	1786
-- 2016	779
-- most apps updated in 2018 then 2017 then 2016


## EDA Summary
-- Imported and analyzed 10,841 apps and 64,295 user reviews using MySQL.
-- Removed 1 corrupted record and handled duplicate apps using ROW_NUMBER().
-- Cleaned and standardized Installs, Size, and Price columns.
-- GAME category recorded the highest installs (13.4B+).
-- Free apps outperformed paid apps in installs and average ratings.
-- Education was the highest-rated category (4.31 average rating).
-- "Everyone" was the dominant content rating category.
-- Sentiment analysis showed generally positive user feedback across categories.
-- Most app updates occurred during 2018.
-- Applied CTEs, Window Functions, Joins, and Date Functions for analysis.

## Business Recommendations

-- Focus on Game, Social, and Entertainment categories for maximum reach.
-- Adopt a freemium model as free apps attract significantly more users.
-- Update apps regularly to improve visibility and user retention.
-- Prioritize user experience to achieve higher ratings and engagement.
-- Monitor review sentiment alongside ratings for better decision-making.
-- Target broader audiences through "Everyone" content-rated apps.
-- Study top-performing apps within each category for feature inspiration.
-- Balance app quality and popularity to drive sustainable growth.

