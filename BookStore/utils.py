import json, hashlib
from BookStore import db
from BookStore.models import User, Book

def add_user(name, email, address, username, sdt, password, avatar):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = User(name=name,
             username=username,
             email=email,
             address=address,
             sdt=sdt,
             password=password,
             avatar=avatar)
    try:
        db.session.add(u)
        db.session.commit()

        return True
    except Exception as ex:
        print(ex)
        return False


def get_book():
    books = Book.query.limit(4).all()
    return books

def get_books():
    booklist = Book.query.limit(20).all()
    return booklist

def get_book_by_id(id):
    book = Book.query.get(id)
    return book


def cart_stats(cart):
    if cart is None:
        return 0, 0
    bookcart = cart.values()
    quantity = sum([p['quantity'] for p in bookcart])
    price = sum([p['price']*p['quantity'] for p in bookcart])
    return quantity, price

