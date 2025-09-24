from app import MovieRepository, MySQLConnection

db = MySQLConnection()
repo = MovieRepository(db)

movie = repo.insert(
    title="Inception",
    director="Christopher Nolan",
    actors="Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page",
    synopsis="A thief enters dreams to steal secrets."
)
print("Inserted:", movie)

for m in repo.list_all():
    print(m)

