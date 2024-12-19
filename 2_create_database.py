import pandas as pd
import sqlite3
import os

def create_database():
    """Create database and required tables"""
    if os.path.exists('unemployment.db'):
        os.remove('unemployment.db')
    
    conn = sqlite3.connect('unemployment.db')
    cursor = conn.cursor()

    # Create time period table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TimePeriod (
        PeriodID INTEGER PRIMARY KEY AUTOINCREMENT,
        PeriodName TEXT NOT NULL UNIQUE
    )
    ''')

    # Create gender table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Gender (
        GenderID INTEGER PRIMARY KEY AUTOINCREMENT,
        GenderName TEXT NOT NULL UNIQUE
    )
    ''')

    # Create region table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Region (
        RegionID INTEGER PRIMARY KEY AUTOINCREMENT,
        RegionName TEXT NOT NULL UNIQUE
    )
    ''')

    # Create unemployment rate by gender table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS UnemploymentRateByGender (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PeriodID INTEGER,
        GenderID INTEGER,
        Rate FLOAT,
        FOREIGN KEY (PeriodID) REFERENCES TimePeriod(PeriodID),
        FOREIGN KEY (GenderID) REFERENCES Gender(GenderID)
    )
    ''')

    # Create unemployment rate by region table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS UnemploymentRateByRegion (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PeriodID INTEGER,
        RegionID INTEGER,
        Rate FLOAT,
        FOREIGN KEY (PeriodID) REFERENCES TimePeriod(PeriodID),
        FOREIGN KEY (RegionID) REFERENCES Region(RegionID)
    )
    ''')

    # Insert base data
    cursor.execute("INSERT INTO Gender (GenderName) VALUES ('Male')")
    cursor.execute("INSERT INTO Gender (GenderName) VALUES ('Female')")
    cursor.execute("INSERT INTO Region (RegionName) VALUES ('UK')")
    cursor.execute("INSERT INTO Region (RegionName) VALUES ('LDN')")

    conn.commit()
    return conn

def import_gender_data(conn, csv_file_path):
    """Import unemployment rate data by gender"""
    try:
        df = pd.read_csv(csv_file_path)
        cursor = conn.cursor()

        for _, row in df.iterrows():
            # Insert time period
            cursor.execute('INSERT OR IGNORE INTO TimePeriod (PeriodName) VALUES (?)', 
                         (row['time'],))
            cursor.execute('SELECT PeriodID FROM TimePeriod WHERE PeriodName = ?', 
                         (row['time'],))
            period_id = cursor.fetchone()[0]

            # Get gender IDs
            cursor.execute('SELECT GenderID FROM Gender WHERE GenderName = ?', ('Male',))
            male_id = cursor.fetchone()[0]
            cursor.execute('SELECT GenderID FROM Gender WHERE GenderName = ?', ('Female',))
            female_id = cursor.fetchone()[0]

            # Insert male unemployment rate
            cursor.execute('''
                INSERT INTO UnemploymentRateByGender (PeriodID, GenderID, Rate)
                VALUES (?, ?, ?)
            ''', (period_id, male_id, row['male']))

            # Insert female unemployment rate
            cursor.execute('''
                INSERT INTO UnemploymentRateByGender (PeriodID, GenderID, Rate)
                VALUES (?, ?, ?)
            ''', (period_id, female_id, row['female']))

        conn.commit()
        print("Gender unemployment rate data imported successfully!")

    except Exception as e:
        print(f"Error importing data: {str(e)}")
        conn.rollback()

def import_region_data(conn, csv_file_path):
    """Import unemployment rate data by region"""
    try:
        df = pd.read_csv(csv_file_path)
        cursor = conn.cursor()

        for _, row in df.iterrows():
            # Insert time period
            cursor.execute('INSERT OR IGNORE INTO TimePeriod (PeriodName) VALUES (?)', 
                         (row['time'],))
            cursor.execute('SELECT PeriodID FROM TimePeriod WHERE PeriodName = ?', 
                         (row['time'],))
            period_id = cursor.fetchone()[0]

            # Get region IDs
            cursor.execute('SELECT RegionID FROM Region WHERE RegionName = ?', ('UK',))
            uk_id = cursor.fetchone()[0]
            cursor.execute('SELECT RegionID FROM Region WHERE RegionName = ?', ('LDN',))
            ldn_id = cursor.fetchone()[0]

            # Insert UK unemployment rate
            cursor.execute('''
                INSERT INTO UnemploymentRateByRegion (PeriodID, RegionID, Rate)
                VALUES (?, ?, ?)
            ''', (period_id, uk_id, row['UK']))

            # Insert London unemployment rate
            cursor.execute('''
                INSERT INTO UnemploymentRateByRegion (PeriodID, RegionID, Rate)
                VALUES (?, ?, ?)
            ''', (period_id, ldn_id, row['LDN']))

        conn.commit()
        print("Regional unemployment rate data imported successfully!")

    except Exception as e:
        print(f"Error importing data: {str(e)}")
        conn.rollback()

def print_database_content(db_path='unemployment.db'):
    """Print database contents"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n=== Unemployment Rate by Gender ===")
        query = '''
        SELECT tp.PeriodName, g.GenderName, ug.Rate
        FROM UnemploymentRateByGender ug
        JOIN TimePeriod tp ON ug.PeriodID = tp.PeriodID
        JOIN Gender g ON ug.GenderID = g.GenderID
        ORDER BY tp.PeriodName, g.GenderName
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(f"Period: {row[0]}, Gender: {row[1]}, Rate: {row[2]}%")
            
        print("\n=== Unemployment Rate by Region ===")
        query = '''
        SELECT tp.PeriodName, r.RegionName, ur.Rate
        FROM UnemploymentRateByRegion ur
        JOIN TimePeriod tp ON ur.PeriodID = tp.PeriodID
        JOIN Region r ON ur.RegionID = r.RegionID
        ORDER BY tp.PeriodName, r.RegionName
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(f"Period: {row[0]}, Region: {row[1]}, Rate: {row[2]}%")
            
        conn.close()
        
    except Exception as e:
        print(f"Error reading database: {str(e)}")

def main():
    # Create database
    conn = create_database()
    
    # Import gender data
    if os.path.exists('q1_gender.csv'):
        import_gender_data(conn, 'q1_gender.csv')
    else:
        print("Gender data file not found")

    # Import region data
    if os.path.exists('q2_region.csv'):
        import_region_data(conn, 'q2_region.csv')
    else:
        print("Region data file not found")
    conn.close()

    print("Database contents:")
    print_database_content()

if __name__ == "__main__":
    main()