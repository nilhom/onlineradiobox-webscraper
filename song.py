class Song:
    def __init__(
            self,
            date,
            time,
            artist,
            title
    ):
        self.date = date
        self.time = time
        self.artist = artist
        self.title = title

    def __str__(self):
        return f"{self.date} {self.time} - {self.artist} - {self.title}"