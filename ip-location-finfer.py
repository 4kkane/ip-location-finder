import sqlite3
import csv
import sys
import ipaddress
import argparse

# Create SQLite database and table

def create_database():
    conn = sqlite3.connect('ip_database.db')  # Create or connect to database file
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ip_data (
        id INTEGER PRIMARY KEY,   -- Primary key and unique index
        start_ip TEXT NOT NULL,
        end_ip TEXT NOT NULL,
        country TEXT,
        province TEXT,
        city TEXT,
        district TEXT,
        isp TEXT
    )
    ''')

    conn.commit()
    conn.close()

# Import data to database
def import_data(file_path):
    conn = sqlite3.connect('ip_database.db')
    cursor = conn.cursor()

    # Open file and read line by line
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)

        # Skip header or empty lines (if any)
        for row in csv_reader:
            if not row or len(row) < 9:  # Ensure row has enough columns
                continue

            # Insert comma-separated fields into database
            try:
                cursor.execute('''
                INSERT INTO ip_data (id, start_ip, end_ip, country, province, city, district, isp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    int(row[0]),    # Index
                    row[2],         # Start IP
                    row[3],         # End IP
                    row[4],         # Country
                    row[5],         # Province
                    row[6],         # City
                    row[7],         # District
                    row[8]          # ISP
                ))
            except sqlite3.IntegrityError as e:
                print(f"Data insertion failed, possibly duplicate ID: {row[0]}, error: {e}")

    conn.commit()
    conn.close()

# Query country, province and other information based on input IP
def query_ip(ip):
    conn = sqlite3.connect('ip_database.db')
    cursor = conn.cursor()

    try:
        # Ensure input is a valid IPv4 address
        ip_addr = int(ipaddress.IPv4Address(ip))

        # Query record with id less than or equal to and closest to ip_addr
        cursor.execute('''
        SELECT id, country, province, city, district, isp FROM ip_data
        WHERE id <= ?
        ORDER BY id DESC LIMIT 1
        ''', (ip_addr,))

        result = cursor.fetchone()
        if result:
            id_value, country, province, city, district, isp = result
            print(f"Query result: ID: {id_value}, Country: {country}, Province: {province}, City: {city}, District: {district}, ISP: {isp}")
        else:
            print("No matching record found!")

    except ValueError:
        print("Please enter a valid IPv4 address!")

    conn.close()

if __name__ == '__main__':
    # Process command line arguments using argparse
    parser = argparse.ArgumentParser(description='IP Address Database Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Import data command
    import_parser = subparsers.add_parser('import', help='Import IP data')
    import_parser.add_argument('file_path', help='CSV file path')

    # Query IP command
    query_parser = subparsers.add_parser('query', help='Query IP information')
    query_parser.add_argument('ip', help='IP address to query')

    args = parser.parse_args()

    if args.command == 'import':
        create_database()
        import_data(args.file_path)
        print("Data import completed!")
    elif args.command == 'query':
        query_ip(args.ip)
    else:
        parser.print_help()
        sys.exit(1)
