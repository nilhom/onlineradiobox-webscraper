import datetime
import sqlite3
import time

from station import Station


def create_table_if_not_exists(conn, station):
    cursor = conn.cursor()

    # Create the table if not exists
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {station.table_name} (
            date DATE,
            time TIME,
            artist TEXT,
            song_name TEXT,
            UNIQUE(date, time, artist, song_name)
        );
    ''')

    conn.commit()


# This scrapes the stations and saves the data collected in the database supplied through conn
def scrape_and_save_to_database(conn, stations):
    cursor = conn.cursor()

    for station in stations:
        create_table_if_not_exists(conn, station)

        errors = set()
        inserted_songs = 0
        for dayNumber in range(1, 7):
            try:
                for entry in station.get_songs():
                    params = (entry.date, entry.time, entry.artist, entry.title)
                    try:
                        cursor.execute(f"INSERT INTO {station.table_name} VALUES (?,?,?,?)", params)
                        inserted_songs += 1
                    except Exception as e:
                        errors.add(str(e))
                time.sleep(1)
            except Exception as e:
                errors.add(str(e))

        print(f'Added {inserted_songs} songs to "{station.urlName}"')


if __name__ == '__main__':
    conn = sqlite3.connect('database.db')

    # Example
    stations = [Station("classicrockflorida", land="us")]
    scrape_and_save_to_database(conn, stations)

    conn.commit()
    conn.close()
