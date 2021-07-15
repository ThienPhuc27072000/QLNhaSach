from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, Enum, ForeignKey
from BookStore import db, admin
from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from BookStore import db
from flask_login import UserMixin, current_user, logout_user
from flask import redirect
from enum import Enum as UserEnum
from sqlalchemy.orm import relationship, backref

class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class Book(db.Model):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    type = Column(String(50))
    author = Column(String(50))
    price = Column(Integer, nullable=False)
    image = Column(String(255), nullable=True)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    sdt = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    joindate = Column(Date, default=datetime.now())
    is_active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    customers = relationship('Customer', backref='user', lazy=True)

    def __str__(self):
        return str(self.id)


class Customer(db.Model):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    sdt = Column(Integer, nullable=False)
    dept = Column(Float(), default=0)
    avatar = Column(String(100))
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipts = relationship('Receipt', backref='receipt', lazy=True)
    bills = relationship('Bill', backref='bill', lazy=True)
    coupons = relationship('Coupon', backref='coupon', lazy=True)


class Receipt(db.Model):
    __tablename__ = "receipt"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_create = Column(Date, default=datetime.now())
    proceeds = Column(Float, default=0)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)


class Bill(db.Model):
    __tablename__ = "bill"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_create = Column(Date, default=datetime.now())
    total = Column(Float, default=0)
    collect = Column(Float, default=0)
    dept = Column(Float, default=0)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)


detail_bill = db.Table("detail_bill",
                       Column('bill_id', Integer, ForeignKey('bill.id'), primary_key=True),
                       Column('book_id', Integer, ForeignKey('book.id'), primary_key=True),
                       Column('quantity', Integer, default=0),
                       Column('price', Float, default=0))


class Inventory_Report(db.Model):
    __tablename__ = "inventory_report"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=datetime.now())


detail_inventory_report = db.Table("detail_inventory_report",
                                   Column('inventory_id', Integer, ForeignKey('inventory_report.id'), primary_key=True),
                                   Column('book_id', Integer, ForeignKey('book.id'), primary_key=True),
                                   Column('inven_before', Integer, default=0),
                                   Column('incurred', String(255), nullable=True),
                                   Column('inven_after', Integer, default=0))


class Debt_Rreport(db.Model):
    __tablename__ = "debt_report"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=datetime.now())


detail_debt_report = db.Table("detail_debt_report",
                              Column('dept_id', Integer, ForeignKey('debt_report.id'), primary_key=True),
                              Column('customer_id', Integer, ForeignKey('customer.id'), primary_key=True),
                              Column('dept_before', Float, default=0),
                              Column('incurred', String(255), default=True),
                              Column('dept_after', Float, default=0))


class Coupon(db.Model):
    __tablename__ = "coupon"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=datetime.now())
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)


detail_coupon = db.Table("detail_coupon",
                         Column('coupon_id', Integer, ForeignKey('coupon.id'), primary_key=True),
                         Column('book_id', Integer, ForeignKey('book.id'), primary_key=True),
                         Column('quantity', Integer, default=0))


class SubModelView(ModelView):
    column_display_pk = True

    def is_accessible(self):
        return current_user.is_authenticated


class ContactView(BaseView):
    @expose("/")
    def __index__(self):
        return self.render("admin/contact.html")

    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


# class BookManagerView(SubModelView):
#     column_labels = dict(id='STT', namebook='Tên sách', typebook='Thể loại sách',
#                          author='Tác giả', price='Giá tiền')
#
# class CustomerView(SubModelView):
#     column_labels = dict(id='STT', fullname='Họ tên', username='Tên đăng nhập', phone='SĐT',
#                          email='Email', joinday='Ngày tham gia', active='Hoạt động')
#

# class InventoryReportView(SubModelView):
#     column_labels = dict(id='STT', topinventory='Tồn đầu', incurred='Phát sinh', finalinventory='Tồn cuối')
#
# class DebtReportView(SubModelView):
#     column_labels = dict(id='STT', topdebt='Nợ đầu', incurred='Phát sinh', finaldebt='Nợ cuối')


# Search in admin
class Search_Book(ModelView):
    column_searchable_list = ('name', 'type', 'author', 'price')
    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(Search_Book(Book, db.session))
# admin.add_view(SubModelView(Customer, db.session))
admin.add_view(ContactView(name="Contact"))
admin.add_view(SubModelView(User, db.session))
admin.add_view(SubModelView(Inventory_Report, db.session, category='Report'))
admin.add_view(SubModelView(Debt_Rreport, db.session, category='Report'))
admin.add_view(LogoutView(name="Logout"))


if __name__ == "__main__":
    db.create_all()