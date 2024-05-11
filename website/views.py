from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import Book
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("Home Page.html", user=current_user)


@views.route('/search')
def search_form():
    query = request.args.get('query')

    if query:
        books = Book.query.filter(Book.title.ilike(f'%{query}%')).all()

        if books:
            return redirect(url_for('views.book_details', book_id=books[0].book_id))
        else:
            return render_template('no_results.html')
    else:
        return redirect(url_for('views.home'))


@views.route('/catalogue')
@login_required
def catalogue():
    books = Book.query.all()
    return render_template("catalogue.html", books=books,
                           user=current_user)


@views.route('/Book Details/<int:book_id>')
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('Book Details.html', book=book)


"""
    Working Progress
@views.route('/AdminDashboard')
def admin_dashboard():
    return render_template("admin/AdminDashboard.html")
"""


"""
Working Progress
@views.route('/Book Details')
def bookDetails():
    title = "Book Details"
    return render_template('Book Details.html', title=title)


@views.route('/Admin Dashboard', methods = ['GET', 'POST'])
def adminDashboard():
    title = "Administrator Dashboard"
    return render_template('AdminDashboard.html', title=title)


@views.route('/User Profile')
def userProfile():
    title = "User Profile"
    return render_template('User Profile.html', title=title)
"""