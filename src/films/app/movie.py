from dataclasses import dataclass

@dataclass
class Movie:
    id: int | None
    title: str
    director: str | None = None
    actors: str | None = None
    synopsis: str | None = None
