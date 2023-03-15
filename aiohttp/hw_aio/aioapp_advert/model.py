from aiohttp.web import HTTPNotFound
from sqlalchemy import URL, DateTime, ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import func

import aioapp_advert.config as config

db_url = URL.create(
    drivername='+'.join([config.DB_DIALECT, config.DB_DRIVER]),
    username=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    port=config.DB_PORT,
    database=config.DB_NAME
)
engine = create_async_engine(db_url, echo=True)
Session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=30), unique=True)
    email: Mapped[str] = mapped_column(String(length=30))
    pwd: Mapped[str] = mapped_column(String(length=300))

    advertisements: Mapped[list['Advertisement']] = relationship(back_populates='user')

    @staticmethod
    async def get(sess, name):
        stmt = await sess.scalar(select(User).where(User.name == name))
        # if not stmt:
        #     raise HTTPNotFound(text='user not found')
        return stmt

    @staticmethod
    async def add(sess, data):
        user = User(**data)
        sess.add(user)
        await sess.commit()


class Advertisement(Base):
    __tablename__ = 'advertisement'

    id = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=30))
    description: Mapped[str] = mapped_column(String(length=300))
    date = mapped_column(DateTime, server_default=func.now())
    owner_id = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship(back_populates='advertisements')

    @staticmethod
    async def get(item_id, session):
        item_id = int(item_id)
        item = await session.get(Advertisement, item_id)
        if not item:
            raise HTTPNotFound(text='item not found')
        return item

    @staticmethod
    async def add(data, session):
        new_item = Advertisement(**data)
        session.add(new_item)
        await session.commit()

    @staticmethod
    async def patch(stmt, data, session):
        for key, val in data.items():
            setattr(stmt, key, val)
        await session.commit()

    @staticmethod
    async def delete(stmt, session):
        await session.delete(stmt)
        await session.commit()
