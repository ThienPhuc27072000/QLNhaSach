from flask import render_template, redirect, request, jsonify, session, url_for
from BookStore import app, login, admin, utils
from BookStore.models import *
from flask_login import login_user, login_required, logout_user
from BookStore import decorator
import hashlib, os
from BookStore.utils import *


@app.route("/")
#@login_required
def index():
    books = get_book()
    return render_template("index.html", books=books)


@app.route("/shop")
def shop():
    books = get_book()
    booklist = get_books()
    return render_template("shop.html", books=books, booklist=booklist)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route("/book-detail/<int:book_id>")
def book_detail(book_id):
    books = get_book()
    book = utils.get_book_by_id(id=book_id)
    return render_template("book-detail.html", book=book, books=books)


@app.route("/register", methods=["GET", "POST"])
def register():
    err_msg = ''
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        sdt = request.form.get('sdt')
        username = request.form.get('username')
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if password == confirm_password:
            avatar = request.files["avatar"]
            avatar_path = 'images/upload/%s' % avatar.filename
            avatar.save(os.path.join(app.config['ROOT_PROJECT_PATH'], 'static/', avatar_path))
            if utils.add_user(name=name, email=email,  address=address, sdt=sdt, username=username,
                              password=password, avatar=avatar_path):
                return render_template("login.html")
        else:
            err_msg = "Mật khẩu KHÔNG khớp!"

    return render_template('register.html', err_msg=err_msg)


@app.route("/login-user")
def login_usr():
    return render_template("login.html")


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id) 


@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(), User.password == password.strip()).first()
        if user:
            login_user(user=user)
    elif request.method == 'GET':
        print(request.url)
        return render_template('login.html')
    
    return redirect("/admin")


@app.route("/login-customer", methods=['GET', 'POST'])
def login_customer():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(), User.password == password.strip()).first()
        if user:
            login_user(user=user)
    elif request.method == 'GET':
        print(request.url)
        return render_template('login.html')

    return render_template("index.html")


@app.route('/logout')
def logout_usr():
    logout_user()
    return redirect(url_for('index'))


@app.route('/payment', methods=['get', 'post'])
@decorator.login_required
def payment():
    if request.method == 'POST':
        if utils.add_receipt(session.get('cart')):
            del session['cart']

            return jsonify({"message": "Payment added!!!"})

    quan, price = utils.cart_stats(session.get('cart'))
    cart_info = {
        'total_quantity': quan,
        'total_amount': price
    }
    return render_template('payment.html', cart_info=cart_info)


@app.route('/searchbook', methods=['GET', 'POST'])
def findbook():
    books = None
    if request.method == "POST":
        searchbook = request.form.get("search")

        books = Book.query.filter(Book.name.contains(searchbook)).all()
    return render_template("searchbook.html", books=books)


@app.route('/api/cart', methods=['GET', 'POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')

    if id in cart:  # có sản phẩm trong giỏ
        quan = cart[id]['quantity']
        cart[id]['quantity'] = int(quan) + 1
    else:   #chưa có sản phẩm trong giỏ
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

        session['cart'] = cart
        quan, price = utils.cart_stats(session['cart'])

        return jsonify({
            "total_amount": price,
            "total_quantity": quan
        })


if __name__ == "__main__":
    # Lấy mã băm
    print(str(hashlib.md5("123".strip().encode("utf-8")).hexdigest()))
    app.run(debug=True)
