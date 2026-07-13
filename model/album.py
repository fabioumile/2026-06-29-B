from dataclasses import dataclass

@dataclass
class Album:
    AlbumId: int
    Title: str
    ArtistId: int
    listaBrani: int
    #.

    def __eq__(self, other):
        return self.AlbumId == other.AlbumId

    def __hash__(self):
        return hash(self.AlbumId)

    def __str__(self):
        return f"{self.Title} - {self.AlbumId}"