from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pprint import pprint
from database_setup import Base, User

engine = create_engine('sqlite:///diary.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

###################CREATE##################################################

# entryBook1 = Book(title = "Володар Перстнів 2", author = "Дж. Толкін",genre='Фентезі',year = 2013)
# entryBook2 = Book(title = "ІТ для чайників", author = "Ноунмейн",genre='Лайфхаки',year = 2015)
# session.add(entryBook1)
# session.add(entryBook2)
# session.commit()


##################READ####################################################
# books = session.query(Book).all() # усі записи

# for b in books:
#     print(b.title)

# book = session.query(Book).first() # перший запис з "голови"

# print(book.title)

# print("")
#books = session.query(Book).filter_by(year=2015).first()

# books.year = 2016
# session.add(books)
# session.commit()

# books = session.query(Book).filter_by(year=2015).first()
# session.delete(books)

# session.commit()
#print(books.id, books.title)


############ ADD USER ##############################
chief_teacher = User(username="admin", email="admin@admin.ua")
chief_teacher.set_password("00000000")
chief_teacher1 = User(username="admin1", email="admin2@admin.ua")
chief_teacher1.set_password("00000001")
session.add_all([chief_teacher,chief_teacher1])
session.commit()