import model
from sqlalchemy import MetaData, create_engine

engine = create_engine(model.db_url)
metadata = MetaData()


def migrate(engine):
    metadata.drop_all(engine)
    metadata.create_all(engine)


if __name__ == '__main__':
    migrate(engine)
