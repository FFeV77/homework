from typing import List
from sqlalchemy import create_engine, String, Integer, ForeignKey, URL, TIMESTAMP, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import func

DB_HOST = '127.0.0.1'
DB_PORT = 8000
DB_DIALECT = 'postgresql'
DB_DRIVER = 'psycopg2'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_NAME = 'advt_db'

db_url = URL.create(
    drivername='+'.join([DB_DIALECT, DB_DRIVER]),
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(db_url, echo=True)


class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=30))
    email: Mapped[str] = mapped_column(String(length=30))
    pwd: Mapped[str] = mapped_column(String(length=30))

    advertisements: Mapped[List['Advertisement']] = relationship(back_populates='user')


class Advertisement(Base):
    __tablename__ = 'advertisement'

    id = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=30))
    description: Mapped[str] = mapped_column(String(length=300))
    date = mapped_column(DateTime, server_default=func.now())
    owner_id = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship(back_populates='advertisements')

    def __repr__(self):
        return {
            'title': self.title,
            'description': self.description,
            'date': self.date
        }

if __name__ == '__main__':
    with engine.connect() as conn:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
