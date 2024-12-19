from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('unemployment.db')
    c = conn.cursor()
    # Create table for gender unemployment data
    c.execute('''CREATE TABLE IF NOT EXISTS gender_unemployment
                 (year INTEGER, male REAL, female REAL)''')
    
    # Import pandas to read the Excel data
    import pandas as pd
    
    # Read the data from Excel file
    df = pd.read_excel('annual-unemployment-region.xlsx', 
                      sheet_name='Gender', 
                      header=[0, 1], 
                      index_col=0, 
                      skiprows=23)
    
    # Prepare the data
    male_data = df['Unemployment rate males - aged 16+']['percent']
    female_data = df['Unemployment rate females - aged 16+']['percent']
    
    # Insert data
    for year, (male, female) in enumerate(zip(male_data, female_data)):
        c.execute("INSERT OR REPLACE INTO gender_unemployment VALUES (?, ?, ?)",
                 (year + 2004, male, female))
    
    conn.commit()
    conn.close()

@app.route('/index')
def welcome():
    conn = sqlite3.connect('unemployment.db')
    c = conn.cursor()
    
    # Get gender unemployment data
    c.execute("""
        SELECT tp.PeriodName, g.GenderName, ug.Rate
        FROM UnemploymentRateByGender ug
        JOIN TimePeriod tp ON ug.PeriodID = tp.PeriodID
        JOIN Gender g ON ug.GenderID = g.GenderID
        ORDER BY tp.PeriodID, g.GenderID
    """)
    gender_data = c.fetchall()
    
    # Get regional unemployment data
    c.execute("""
        SELECT tp.PeriodName, r.RegionName, ur.Rate
        FROM UnemploymentRateByRegion ur
        JOIN TimePeriod tp ON ur.PeriodID = tp.PeriodID
        JOIN Region r ON ur.RegionID = r.RegionID
        ORDER BY tp.PeriodID, r.RegionID
    """)
    region_data = c.fetchall()
    conn.close()
    
    return render_template('index.html', 
                         gender_data=gender_data, 
                         region_data=region_data)

@app.route('/gender_analysis')
def show_data():
    conn = sqlite3.connect('unemployment.db')
    c = conn.cursor()
    c.execute("SELECT year, male, female FROM gender_unemployment ORDER BY year")
    gender_data = c.fetchall()
    conn.close()
    return render_template('gender_analysis.html', gender_data=gender_data)

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('unemployment.db')
    c = conn.cursor()
    
    # Fetch gender unemployment data
    c.execute("SELECT year, male, female FROM gender_unemployment ORDER BY year")
    gender_data = c.fetchall()
    
    # Fetch regional unemployment data (assuming you have this table)
    c.execute("""
        SELECT tp.PeriodName, r.RegionName, ur.Rate
        FROM UnemploymentRateByRegion ur
        JOIN TimePeriod tp ON ur.PeriodID = tp.PeriodID
        JOIN Region r ON ur.RegionID = r.RegionID
        ORDER BY tp.PeriodID, r.RegionID
    """)
    region_data = c.fetchall()
    
    # Fetch London-specific trend (assuming you have this data)
    c.execute("""
        SELECT tp.PeriodName, ur.Rate
        FROM UnemploymentRateByRegion ur
        JOIN TimePeriod tp ON ur.PeriodID = tp.PeriodID
        JOIN Region r ON ur.RegionID = r.RegionID
        WHERE r.RegionName = 'LDN'
        ORDER BY tp.PeriodID
    """)
    london_data = c.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html',
                         gender_data=gender_data,
                         region_data=region_data,
                         london_data=london_data)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/check-data')
def check_data():
    conn = sqlite3.connect('unemployment.db')
    c = conn.cursor()
    c.execute("SELECT * FROM gender_unemployment ORDER BY year")
    all_data = c.fetchall()
    conn.close()
    
    # Format the data as HTML table
    html = '<h2>All Data in gender_unemployment table</h2>'
    html += '<table border="1"><tr><th>Year</th><th>Male %</th><th>Female %</th></tr>'
    for row in all_data:
        html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>'
    html += '</table>'
    return html

if __name__ == '__main__':
    # Initialize the database
    init_db()
    # Run the Flask app
    app.run(debug=True) 