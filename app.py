from models import (Base, session, Book, engine)

#  main menu
#  add, search, analysis, exit, view
#  add books to the database
#  edit books
#  delete books
#  search function
#  data cleaning function
#  loop runs program until exit


if __name__ == '__main__':
    #  create database
    Base.metadata.create_all(engine)