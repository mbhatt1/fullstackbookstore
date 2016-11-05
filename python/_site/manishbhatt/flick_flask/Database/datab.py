#-*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, scoped_session



eng = create_engine('sqlite:///bookstore.db')

Session = scoped_session(sessionmaker(bind=eng))

Base = declarative_base()

ses = Session()

class Book(Base):

	__tablename__='Book'
	Id = Column(Integer, primary_key=True)
	Name = Column(String)
	Seller = relationship('Seller')
	Seller_email = Column(String, ForeignKey("Seller.Id"))
	department = Column(String(4))
	course = Column (String(4))
	photoid = Column(String)

	def __init__(self, Id, Name, Seller_email, department, course, photoid):
		self.Id=Id
		self.Name = Name
		self.Seller_email = Seller_email
		self.department = department
		self.course = course
		self.photoid=photoid


class Seller(Base):

	__tablename__= "Seller"
	Book = relationship("Book")
	Id = Column (String, primary_key=True)
	passwd = Column (String)
	Seller_firstname = Column (String(10))
	Seller_lastname = Column (String(10))
	department = Column (String(4))
	booksSold = []

	def __init__(self, Id, passwd, Seller_firstname, Seller_lastname, department):
		self.Id = Id
		self.passwd = passwd
		self.Seller_firstname = Seller_firstname
		self.Seller_lastname = Seller_lastname
		self.department = department


Base.metadata.create_all(eng)
	




def get_seller_email_password(Email="test@uno.edu", passwd="password"):
	res = ses.query(Seller).filter(Seller.Id == Email)

	if (res is not None):
		for user in res:
			if (user.passwd == passwd):
				return 0 #the username and password found
			else:
				return -1 #the password doesn't match
	return -2



def get_books_by_email(Email="a@uno.edu"):
	res = ses.query(Book).filter(Book.Seller_email == Email)
	return res

#-1 means that length not correct

def get_books_by_department(Department):

	res = ses.query(Book).filter(Book.department == Department)
	return res

def get_books_by_Id(Id):

	res = ses.query(Book).filter(Book.Id == Id)
	return res


def get_books_by_course (course="2221"):

	res = ses.query(Book).filter(Book.course == course)
	return res



#-1 means the user already exists
def set_seller(Email="email", passwd="password", firstName="FirstName", lastName="LastName", department="department"):
	
	ses.add_all([Seller(Id=Email, passwd=passwd, Seller_firstname=firstName, Seller_lastname=lastName, department=department)])
	ses.commit()
	return 0



#-1 means bad length, -2 means same book by same seller is listed
def set_book(Name = "name", Seller_email = "sellEmail", department = "depa", course = "cour", photoid="saddsads"):


	res = ses.query(Book).all()
	totalBook = len(res)
	ses.add_all([Book(Id = totalBook+1, Name = Name, Seller_email = Seller_email, department = department, course = course, photoid=photoid)])
	ses.commit()
	return 0


def get_all_books():
	res = ses.query(Book).all()
	return res

def shutdown():
	ses.remove()

