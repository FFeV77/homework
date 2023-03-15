from sqlalchemy import (create_engine, String, Integer,
                        ForeignKey, URL, DateTime)
from sqlalchemy.orm import (DeclarativeBase, Mapped, Session,
                            mapped_column, relationship)
from sqlalchemy.sql.expression import func
import config


db_url = URL.create(
    drivername='+'.join([config.DB_DIALECT, config.DB_DRIVER]),
    username=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    port=config.DB_PORT,
    database=config.DB_NAME
)
engine = create_engine(db_url, echo=True)
Session = Session(engine)


class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=30), unique=True)
    email: Mapped[str] = mapped_column(String(length=30))
    pwd: Mapped[str] = mapped_column(String(length=300))

    advertisements: Mapped[list['Advertisement']] = relationship(back_populates='user')


class Advertisement(Base):
    __tablename__ = 'advertisement'

    id = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=30))
    description: Mapped[str] = mapped_column(String(length=300))
    date = mapped_column(DateTime, server_default=func.now())
    owner_id = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship(back_populates='advertisements')


if __name__ == '__main__':
    with engine.connect() as conn:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
