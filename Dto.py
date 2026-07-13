""""
#Arco altezza model
from dataclasses import dataclass
@dataclass
class Arco:
    a1: Artista
    a2: Artista
    peso: int

# DTO
# fa da datacontine, al liv  del model
# sul database clicco sulla tabella , shift freccia in giu copio e incollo
from dataclasses import dataclass
from datetime import datetime
    @dataclass
    class Movie:
        id: str
        title: str
        year: int
        date_published: datetime
        duration: int
        country: str
        worlwide_gross_income: str
        languages: str
        production_company: str

        def __eq__(self, other):
            return self.id == other.id

        def __hash__(self):
            return hash(self.id)

        def __str__(self):
            return f"{self.title} - {self.production_company}"

from dataclasses import dataclass
import datetime from datetime
    @dataclass
    class Names:
        id: str
        name: str
        height: int
        date_of_birth: datetime
        known_for_movies: str

        def __eq__(self, other):
            return self.id == other.id

        def __hash__(self):
            return hash(self.id)

        def __str__(self):
            return f"{self.name} - {self.known_for_movies}"

from dataclasses import dataclass
    @dataclass
    class Ratings:
        movie_id: str
        avg_rating: float
        total_votes: int
        median_rating: int

        def __eq__(self, other):
            return self.movie_id == other.movie_id

        def __hash__(self):
            return hash(self.movie_id)

        def __str__(self):
            return f"{self.movie_id} - {self.avg_rating}"

from dataclasses import dataclass
    @dataclass
    class Genre:
        movie_id:str
        genre: str

        def __eq__(self, other):
            return self.movie_id == other.movie_id

        def __hash__(self):
            return hash(self.movie_id)

        def __str__(self):
            return f"{self.movie_id} - {self.genre}"

from dataclasses import dataclass
    @dataclass
    class Rolemapping:
        movie_id: str
        name_id: str
        category: str

        def __eq__(self, other):
            return self.movie_id == other.movie_id

        def __hash__(self):
            return hash(self.movie_id)

        def __str__(self):
            return f"{self.movie_id} - {self.category}"

from dataclasses import dataclass
    @dataclass
    class Rolemapping:
        movie_id: str
        name_id: str

        def __eq__(self, other):
            return self.movie_id == other.movie_id

        def __hash__(self):
            return hash(self.movie_id)

        def __str__(self):
            return f"{self.movie_id} - {self.name_id}"

"""