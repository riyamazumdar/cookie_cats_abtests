CREATE DATABASE IF NOT EXISTS cookie_cats_ab;

USE cookie_cats_ab;

--table
CREATE TABLE player_data(
    userid BIGINT,
    version VARCHAR(10),
    sum_gamegrounds INT,
    retention_1 VARCHAR(10),
    retention_7 VARCHAR(10),
);

--loading data
LOAD DATA LOCAL INFILE 'C:/Users/KIIT/Desktop/projects/cookiecats/cookie_cats.csv' 
    INTO TABLE player_data  
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;

-- converting retention values to boolean so we are able to perform mathematical functions
UPDATE player_data SET retention_1 = (retention_1='True');
UPDATE player_data SET retention_7 = (retention_7='True');

--Sample Ratio Mismatch(SRM)- this confirms gate_30/gate_40 is balanced
SELECT
    version,
    COUNT(*) AS n_players,
    ROUND(COUNT(*)*100.0/ SUM(COUNT(*)) OVER(), 2) AS pct_of_total
FROM player_data;
GROUP BY version;

--Actual retention comparison
SELECT version,
         COUNT(*) AS n_players, 
         SUM(retention_1) AS retained_day1, 
         ROUND(SUM(retention_1)*100.0/ COUNT(*),2) AS retention_1_pct, 
         SUM(retention_7) AS retained_day7, 
         ROUND(SUM(retention_7)*100.0/ COUNT(*), 2) AS retention_7_pct, 
         ROUND(AVG(sum_gamerounds),1) AS avg_gamerounds 
FROM player_data 
GROUP BY version;