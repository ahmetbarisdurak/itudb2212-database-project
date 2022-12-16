import sqlite3
from flask import Flask, render_template, request, redirect, url_for, abort, flash
import random


app = Flask(__name__, template_folder='templates', static_folder='static')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

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
    
    tableName = request.form["edit"]

    conn = get_db_connection()
    
    countryInfo = conn.execute('SELECT * FROM ' + tableName).fetchall()

    conn.close()

    for country in countryInfo:
        if(int(countryIndex) == country['countryIndex']):
            countryEdit = country


    return render_template('editPage.html', countryEdit=countryEdit, tableName=tableName)

@app.route('/<tableName>/changeValues', methods=('GET', 'POST'))
def changeValues(tableName):
    
    print(tableName)

    values = request.form.getlist('countryFeatures')
    
    print(values)

    for value in values:
        print("-->" + value + "<--")

    conn = get_db_connection()
    if(tableName == 'generalInfo'):
        conn.execute('UPDATE generalInfo SET countryName="' + values[0] 
        + '", region="' + values[1] 
        + '", countryPopulation=' + values[2] 
        + ', capital="' + values[3] 
        + '", currency="' + values[4] 
        + '", exchangeRate=' + values[5]) 
    elif(tableName == 'countryPopulations'):
        conn.execute('UPDATE countryPopulations SET populationGrowth=' + values[0] 
        + ', urbanPopulation=' + values[1] 
        + ', fertility=' + values[2] 
        + ', femaleLifeExpectancy=' + values[3] 
        + ', maleLifeExpentancy=' + values[4] 
        + ', refugeesOthers=' + values[5])
    conn.commit()
    conn.close()
    
    return redirect(url_for('countryInformation'))
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

    if(inputData[0] == inputData[1]):
        print('Countries can''t be same')
        return redirect(url_for('countryComparator'))

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
    conn = get_db_connection()
    countries = conn.execute('SELECT * FROM generalInfo').fetchall()
    conn.close()
    return render_template('currencyExchange.html', countries=countries)

@app.route('/calculateValue', methods=['GET', 'POST'])
def calculateValue():

    inputData = list(request.form.values())

    conn = get_db_connection()
    countries = conn.execute('SELECT * FROM generalInfo').fetchall()
    conn.close()

    if(inputData[0] == inputData[2]):
        print('Countries can''t be same')
        return redirect(url_for('currencyExchange'))


    for country in countries:
        if(inputData[0] == country['countryName']):
            exchangeRate1 = country['exchangeRate']
            country1 = country
        elif(inputData[2] == country['countryName']):
            exchangeRate2 = country['exchangeRate']
            country2 = country

    value = exchangeRate1 * float(inputData[1])
    value = value / exchangeRate2

    
    return render_template('calculatedValue.html',country1=country1, country2=country2, value=value)

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
