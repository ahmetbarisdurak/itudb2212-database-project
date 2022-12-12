import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import random


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def homePage():
    return render_template("base.html")

@app.route('/info')
def countryInformation():
    conn = get_db_connection()
    countries = conn.execute('SELECT * \
                            FROM generalInfo JOIN countryPopulations \
                            ON generalInfo.countryIndex = countryPopulations.countryIndex \
                                  ').fetchall()
    conn.close()
    return render_template('countryInfo.html', countries=countries)

@app.route('/showInfo', methods=['GET', 'POST'])
def showInfo():
    inputData = list(request.form.values())
    # Burada datayı rahat bir şekilde alabiliyorum.
    conn = get_db_connection()
    countries = conn.execute('SELECT * \
                            FROM generalInfo JOIN countryPopulations \
                            ON generalInfo.countryIndex = countryPopulations.countryIndex \
                                  ').fetchall()
    conn.close()

    for country in countries:
        if(inputData[0] == country['countryName']):
            country1 = country

    print(country1.keys())

    return render_template('showInfo.html', country=country1)
@app.route('/comparison')
def countryComparator():
    conn = get_db_connection()
    countries = conn.execute('SELECT * FROM generalInfo').fetchall()
    conn.close()
    return render_template('countryComparator.html', countries=countries)

@app.route("/compare", methods=['GET', 'POST'])
def compare():
    inputData = list(request.form.values())
    print(inputData[0] + " is input data 0")
    print(inputData[1] + " is input data 1")
    conn = get_db_connection()
    countries = conn.execute('SELECT * \
                            FROM generalInfo JOIN countryPopulations \
                            ON generalInfo.countryIndex = countryPopulations.countryIndex \
                                  ').fetchall()
    conn.close()

    for country in countries:
        if(inputData[0] == country['countryName']):
            country1 = country
        elif(inputData[1] == country['countryName']):
            country2 = country

    print(countries)

    return render_template('comparisonPage.html', country1=country1, country2=country2)

@app.route('/exchange')
def currencyExchange():
    print("Currency Exchange")

@app.route('/randomInfo')
def randomInfo():
    conn = get_db_connection()
    countries = conn.execute('SELECT * FROM generalInfo').fetchall()
    conn.close()

    
    randomCountry = random.randint(0,len(countries) - 1)
    randomIndex = random.randint(0, len(countries[0]) - 1)
    
    print(" random country is (?)", randomCountry)
    print("random index is (?)", randomIndex)

    print(countries[randomCountry].keys())

    text = "Did you know that " + (countries[randomCountry].keys())[randomIndex]+ " of " 
    text = text + countries[randomCountry]["countryName"]  
    text = text + " is " + str(countries[randomCountry][randomIndex])

    return render_template('randomInfo.html', text=text)

@app.route('/ranking')
def countryRanking():
    print("country ranking")