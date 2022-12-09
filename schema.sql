DROP TABLE IF EXISTS generalInfo;

CREATE TABLE generalInfo (
    countryIndex INTEGER PRIMARY KEY AUTOINCREMENT,
    countryName VARCHAR(80),
    region VARCHAR(30),
    countryPopulation INTEGER,
    capital VARCHAR(40),
    currency VARCHAR(10),
    exchangeRate FLOAT
);

DROP TABLE IF EXISTS population;

CREATE TABLE population (
    countryIndex INTEGER,
    populationGrowth FLOAT,
    urbanPopulation FLOAT,
    fertility FLOAT,
    femaleLifeExpectancy FLOAT,
    maleLifeExpentancy FLOAT ,
    refugeesOthers FLOAT,
    worldOrder INTEGER PRIMARY KEY,
    
    FOREIGN KEY(countryIndex) REFERENCES generalInfo(countryIndex)
);