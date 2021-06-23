#  create a database
#  give it a name (books.db)
#  create the model
#  columns: title, author, date published, price

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///books.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column('Title', String)
    author = Column('Author', String)
    date_published = Column('Published', Date)
    price = Column('Price', Integer)

    def __repr__(self):
        return f'<User(Title: {self.title}, Author: {self.author},' \
               f'Published: {self.date_published}, Price: ${self.price}>'


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    # rachel_user = User(name='Rachel', fullname='Rachel Johnson', nickname='Ray')
    # session.add(rachel_user)
    # print(rachel_user.name)
    # print(rachel_user.id)
    # session.commit()

    # session.add_all([
    #     User(name='Grace', fullname='Grace Hopper', nickname='Pioneer'),
    #     User(name='Alan', fullname='Alan Turing', nickname='Computer Scientist'),
    #     User(name='Katherine', fullname='Katherine Johnson', nickname='')
    #     ])
    # session.commit()
