import sqlite3

def check_database():
    try:
        # Connect to the database
        conn = sqlite3.connect('unemployment.db')
        cursor = conn.cursor()
        
        # Check what tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("\nTables in database:")
        for table in tables:
            print(table[0])
            
        # For each table, show its structure
        for table in tables:
            print(f"\nStructure of {table[0]}:")
            cursor.execute(f"PRAGMA table_info({table[0]})")
            columns = cursor.fetchall()
            for col in columns:
                print(f"Column: {col[1]} ({col[2]})")
            
            # Show sample data
            print(f"\nSample data from {table[0]}:")
            cursor.execute(f"SELECT * FROM {table[0]} LIMIT 3")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            
    except sqlite3.OperationalError as e:
        print("Error:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    check_database() 