from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Borrow, Book, User
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
def index_redirect():
  return redirect(url_for('views.home'))


@views.route('/home')
@login_required
def home():
   return render_template('home.html', user=current_user)


@views.route('/books')
@login_required
def books():
   q = request.args.get('q', '').strip()
   if q:
# simple search in title or author
    books = Book.query.filter((Book.title.ilike(f'%{q}%')) | (Book.author.ilike(f'%{q}%'))).all()
   else:
    books = Book.query.all()
   return render_template('books.html', user=current_user, books=books, q=q)

@views.route('/borrow_history')
@login_required
def borrow_history():
    borrows = Borrow.query.filter_by(user_id=current_user.id).order_by(Borrow.borrowed_at.desc()).all()
    return render_template('borrow_history.html', user=current_user, borrows=borrows)
# Admin dashboard
@views.route('/admin')
@login_required
def admin_dashboard():
   if not current_user.is_admin:
     flash('Access denied', 'danger')
     return redirect(url_for('views.home'))
   books = Book.query.all()
   return render_template('admin_dashboard.html', user=current_user, books=books)

@views.route('/admin/book/new', methods=['GET', 'POST'])
@login_required
def admin_create_book():
    if not current_user.is_admin:
      flash('Access denied', 'danger')
      return redirect(url_for('views.home'))
    if request.method == 'POST':
       title = request.form.get('title')
       author = request.form.get('author')
       description = request.form.get('description')
       stock = int(request.form.get('stock') or 0)
       book = Book(title=title, author=author, description=description, stock=stock)
       db.session.add(book)
       db.session.commit()
       flash('Book added', 'success')
       return redirect(url_for('views.admin_dashboard'))
    return render_template('admin_create_book.html', user=current_user)
@views.route('/admin/book/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_book(id):
   if not current_user.is_admin:
     flash('Access denied', 'danger')
     return redirect(url_for('views.home'))
   book = Book.query.get_or_404(id)
   if request.method == 'POST':
      book.title = request.form.get('title')
      book.author = request.form.get('author')
      book.description = request.form.get('description')
      book.stock = int(request.form.get('stock') or 0)
      db.session.commit()
      flash('Book updated', 'success')
      return redirect(url_for('views.admin_dashboard'))
   return render_template('admin_edit_book.html', user=current_user, book=book)
@views.route('/admin/book/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_book(id):
   if not current_user.is_admin:
     flash('Access denied', 'danger')
     return redirect(url_for('views.home'))
   book = Book.query.get_or_404(id)
   db.session.delete(book)
   db.session.commit()
   flash('Book deleted', 'info')
   return redirect(url_for('views.admin_dashboard')) 
# Borrow a Book (via button on /books)
@views.route('/books', methods=['POST'])
@login_required
def borrow_book():
    book_id = request.form.get('book_id')

    if not book_id:
        flash('Missing book ID', 'danger')
        return redirect(url_for('views.books'))

    book = Book.query.get(book_id)
    if not book:
        flash('Book not found', 'danger')
        return redirect(url_for('views.books'))

    if book.stock <= 0:
        flash('No stock available for this book', 'danger')
        return redirect(url_for('views.books'))
# Create a new borrow record
    borrow = Borrow(user_id=current_user.id, book_id=book.id)
    book.stock -= 1  # Decrease available stock

    db.session.add(borrow)
    db.session.commit()

    flash(f'You borrowed "{book.title}" successfully!', 'success')
    return redirect(url_for('views.borrow_history'))
# Return a Borrowed Book
# -----------------------------
@views.route('/return/<int:borrow_id>', methods=['POST'])
@login_required
def return_book(borrow_id):
    borrow = Borrow.query.get_or_404(borrow_id)

    # Check that the user owns this borrow (or is admin)
    if borrow.user_id != current_user.id and not current_user.is_admin:
        flash('Not authorized to return this book', 'danger')
        return redirect(url_for('views.borrow_history'))

    # If already returned
    if borrow.returned:
        flash('This book is already returned', 'info')
        return redirect(url_for('views.borrow_history'))

    # Mark as returned
    borrow.returned = True
    borrow.returned_at = datetime.utcnow()
    borrow.book.stock += 1  # Add back to stock

    db.session.commit()
    flash(f'You returned "{borrow.book.title}" successfully!', 'success')
    return redirect(url_for('views.borrow_history'))