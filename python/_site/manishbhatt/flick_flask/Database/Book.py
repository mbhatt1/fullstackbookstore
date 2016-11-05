from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker


Base = declarative_base()



class Book(Base):

	__tablename__='Book'
	Id = Column(Integer, primary_key=True)
	Name = Column(String)
	Seller = relationship('Seller')
	Seller_email = Column(String, ForeignKey("Seller.Id"))
	department = Column(String(4))
	course = Column (String(4))

	def __init__(self, Id, Name, Seller_email, department, course):
		self.Id=Id
		self.Name = Name
		self.Seller_email = Seller_email
		self.department = department
		self.course = course


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
		self.department = departmen