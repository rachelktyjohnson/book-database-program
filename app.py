from models import (Base, session, Book, engine)
import csv
import datetime
import time
from sqlalchemy import desc

#  main menu
#  add, search, analysis, exit, view
#  add books to the database
#  edit books
#  delete books
#  search function
#  data cleaning function
#  loop runs program until exit


def menu():
    while True:
        print('''
            \nPROGRAMMING BOOKS
            \r1) Add Book
            \r2) View all books
            \r3) Search for book
            \r4) Book analysis
            \r5) Exit
        ''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            print("Please choose one of the options above (1-5)!!")


def submenu():
    while True:
        print('''
            \r1) Edit
            \r2) Delete
            \r3) Return to Main Menu
        ''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("Please choose one of the options above (1-3)!!")


def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']

    try:
        split_date = date_str.split(' ')
        #  ['July', '1,', '2013']

        day = int(split_date[1].split(',')[0])
        #  ['1', '']

        month = int(months.index(split_date[0]) + 1)
        year = int(split_date[2])

        return_date = datetime.date(year, month, day)
    except ValueError:
        print('''
            \nDATE ERROR! The date format should be valid
            \n(Ex: October 25, 2010)
            \nPress ENTER to try again
        ''')
        return
    except IndexError:
        print('''
            \nDATE ERROR! The date format should be valid
            \n(Ex: October 25, 2010)
            \nPress ENTER to try again
        ''')
        return
    else:
        return return_date


def clean_price(price_str):
    try:
        price_float = float(price_str)
        #  return it as cents so we don't have any decimal points
        return_int = int(price_float*100)
    except ValueError:
        print('''
                    \nPRICE ERROR! The number format should be valid with no $ sign
                    \n(Ex: 10.99)
                    \nPress ENTER to try again
                ''')
    else:
        return return_int


def edit_check(column_name, current_value):
    print(f'EDIT {column_name}')
    if column_name == 'Price':
        print(f'Current Value: {current_value/100}')
    elif column_name == 'Date':
        print(f'Current Value: {current_value.strftime("%B %d, %Y")}')
    else:
        print(f'Current Value: {current_value}')

    if column_name == 'Date' or column_name == 'Price':
        while True:
            changes = input('What would you like to change the value to? ')
            if column_name == 'Date':
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            elif column_name == 'Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
    else:
        return input('What would you like to change the value to? ')


def add_csv():
    #  open the CSV file
    with open('suggested_books.csv') as csv_file:
        data = csv.reader(csv_file)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title == row[0]).one_or_none()
            if book_in_db is None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, date_published=date, price=price)
                session.add(new_book)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            #  add book

            title = input("Title: ")

            author = input("Author: ")

            date_error = True
            date = None
            while date_error:
                date = input("Published Date (ex: October 25, 2021): ")
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False

            price_error = True
            price = None
            while price_error:
                price = input("Price (ex: 26.54): ")
                price = clean_price(price)
                if type(price) == int:
                    price_error = False

            new_book = Book(title=title, author=author, date_published=date, price=price)
            session.add(new_book)
            session.commit()
            print(f'The book, {title}, was added!')
            time.sleep(1.5)

        elif choice == '2':
            #  view all books
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author}')
        elif choice == '3':
            #  search for book
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            id_choice = None
            while id_error:
                print(f'ID Options: {id_options}')
                id_choice = int(input("Book ID: "))
                if id_choice in id_options:
                    id_error = False
            the_book = session.query(Book).filter(Book.id == id_choice).first()
            print(f'{the_book.title}, by {the_book.author}')
            print(f'Published: {the_book.date_published}')
            print(f'Price: ${the_book.price / 100}')
            sub_choice = submenu()
            if sub_choice == '1':
                #  edit
                the_book.title = edit_check('Title', the_book.title)
                the_book.author = edit_check('Author', the_book.author)
                the_book.date_published = edit_check('Date', the_book.date_published)
                the_book.price = edit_check('Price', the_book.price)
                session.commit()
                print('Book updated!')
                time.sleep(2)
            elif sub_choice == '2':
                session.delete(the_book)
                session.commit()
                print("Book deleted")
                time.sleep(1.5)
        elif choice == '4':
            #  book analysis
            oldest_book = session.query(Book).order_by(Book.date_published).first()
            newest_book = session.query(Book).order_by(Book.date_published.desc()).first()
            total_books = session.query(Book).count()
            python_books = session.query(Book).filter(Book.title.like('%python%')).count()
            print('BOOK ANALYSIS')
            print("Oldest book: {}".format(oldest_book.title))
            print("Newest book: {}".format(newest_book.title))
            print("Total books: {}".format(total_books))
            print("Total Python books: {}".format(python_books))
        else:
            print("Goodbye!")
            app_running = False


if __name__ == '__main__':
    #  create database
    Base.metadata.create_all(engine)
    app()
    #  add_csv()

