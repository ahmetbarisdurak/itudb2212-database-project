import sqlite3

def readSQL(filename: str) -> list:
    with open(filename, 'r') as f:
        content = f.readlines()
    return content


connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

#cur.execute("INSERT INTO generalInfo (countryIndex, countryName, region, countryPopulation, capital, currency, exchangeRate ) VALUES (1, 'Armenia', 'Western Asia', 2968, 'Yerevan', 'AMD', 522.6)")

#cur.execute("INSERT INTO generalInfo (countryIndex, countryName, region, countryPopulation, capital, currency, exchangeRate ) VALUES (2, 'Argentina', 'South America', 45606, 'Buenos Aires', 'ARS', 84)")


createStatements = readSQL('createStatements.sql')
for statement in createStatements:
    print(statement)
    if len(statement) > 5:
        cur.execute(statement)
        

connection.commit()
connection.close()
