# Webscraper for onlineradiobox.com

This project takes a list of radio stations from the Website https://onlineradiobox.com/ and saves the songs played on these stations in the database.db file.

# Database file Schema

```SQL
date DATE,
time TIME,
artist TEXT,
song_name TEXT,
UNIQUE(date, time, artist, song_name)
```
