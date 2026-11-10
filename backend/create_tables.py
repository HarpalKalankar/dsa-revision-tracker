from database import Base, engine
import models  # noqa: F401  (importing registers the tables)

Base.metadata.create_all(engine)
print("Tables created")