import sqlite3
from flask import Flask, render_template, request, redirect, url_for, abort, flash
import random


app = Flask(__name__, template_folder='templates', static_folder='static')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def getCountry(tableName, countryIndex):
    conn = get_db_connection()
    country = conn.execute('SELECT * FROM ? WHERE id = ?',
                        (tableName, countryIndex)).fetchone()
    conn.close()
    if country is None:
        abort(404)
    return country

@app.route('/')
def homePage():
    conn = get_db_connection()
    countries = conn.execute('SELECT * FROM generalInfo').fetchall()
    conn.close()
    
    return render_template("base.html", countries=countries)

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
    
    print(inputData)
    conn = get_db_connection()
    
    countryInfo = conn.execute('SELECT * FROM generalInfo').fetchall()
    countryPopulations = conn.execute('SELECT * FROM countryPopulations').fetchall()

    conn.close()

    for country in countryInfo:
        if(inputData[0] == country['countryName']):
            countryInfo = country
            countryIndex = country['countryIndex']

    for country in countryPopulations:
        if(countryIndex == country['countryIndex']):
            countryPopulations = country
    
    return render_template('showInfo.html', countryInfo=countryInfo,
        countryPopulations=countryPopulations)

@app.route('/listCountries')
def listCountries():
    conn = get_db_connection()
    countries = conn.execute('SELECT * FROM generalInfo').fetchall()
    conn.close()
    
    return render_template("listCountries.html", countries=countries) 

@app.route('/<countryIndex>/editCountry', methods=('GET', 'POST'))
def editCountry(countryIndex):
 
    print("yessir")
    print(countryIndex)

    return render_template('editPage.html')

@app.route('/comparison')
def countryComparator():
    conn = get_db_connection()
    countries = conn.execute('SELECT * FROM generalInfo').fetchall()
    conn.close()
    return render_template('countryComparator.html', countries=countries)

@app.route("/compare", methods=['GET', 'POST'])
def compare():
    inputData = list(request.form.values())
    tableSelection = request.form['tables']

    conn = get_db_connection()
    countries = conn.execute("SELECT * FROM " + tableSelection).fetchall()
    conn.close()

    for country in countries:
        if(inputData[0] == country['countryName']):
            country1 = country
        elif(inputData[1] == country['countryName']):
            country2 = country

    return render_template('comparisonPage.html', country1=country1, country2=country2)

@app.route('/exchange')
def currencyExchange():
    print("Currency Exchange")

@app.route('/randomInfo')
def randomInfo():
    conn = get_db_connection()
    countries = conn.execute('SELECT * \
                            FROM generalInfo JOIN countryPopulations \
                            ON generalInfo.countryIndex = countryPopulations.countryIndex \
                                 ').fetchall()
    conn.close()

    
    
    randomCountry = random.randint(0,len(countries) - 1)
    randomIndex = random.randint(0, len(countries[0]) - 1)

    while(countries[randomCountry].keys()[randomIndex] == "countryName" or \
     countries[randomCountry].keys()[randomIndex] == "countryIndex" ):

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

@app.route("/delete", methods=['GET', 'POST'])
def delete():
    inputData = list(request.form.getlist('countryDeletion'))
    
    willDelete = []

    conn = get_db_connection()
    countries = conn.execute('SELECT * FROM generalInfo').fetchall()
    conn.commit()
    
    for x in inputData:
        for country in countries:
            if(country['countryName'] == x):  
                willDelete.append(country['countryIndex'])

    for i in willDelete:
        countries = conn.execute('DELETE FROM generalInfo WHERE countryIndex = ?', (i,))
        conn.commit()

    conn.close()

    return redirect(url_for('listCountries'))
