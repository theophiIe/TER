from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from table import Base

engine = create_engine(f"postgresql://postgres@/lessurligneurs")
print(database_exists(engine.url))
if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))

session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


if __name__ == '__main__':
    pass
