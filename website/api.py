from flask import Blueprint, request, jsonify, current_app
from .models import User, Book, Borrow
from . import db
import jwt
from werkzeug.security import check_password_hash
from functools import wraps
from datetime import datetime, timedelta


api = Blueprint('api', __name__)
# Helper: create JWT
def create_token(user):
  payload = {
        'user_id': user.id,
          'exp': datetime.utcnow() + timedelta(hours=12)
    }
  token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
  return token
# Auth: token endpoint
@api.route('/token', methods=['POST'])
def get_token():
   data = request.json or {}
   email = data.get('email')
   password = data.get('password')
   if not email or not password:
     return jsonify({'error': 'Email and password required'}), 400
   user = User.query.filter_by(email=email).first()
   if not user or not check_password_hash(user.password, password):
      return jsonify({'error': 'Invalid credentials'}), 401
   token = create_token(user)
   return jsonify({'token': token})
# Decorator to protect endpoints with JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
      auth = request.headers.get('Authorization', None)
      if not auth:
       return jsonify({'error': 'Token missing'}), 401
      parts = auth.split()
      if parts[0].lower() != 'bearer' or len(parts) != 2:
        return jsonify({'error': 'Authorization header must be Bearer token'}), 401
      token = parts[1]
      try:
           data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
           user_id = data.get('user_id')
           user = User.query.get(user_id)
           if not user:
             return jsonify({'error': 'User not found'}), 401
# attach user to request context
           request._jwt_user = user
      except jwt.ExpiredSignatureError:
           return jsonify({'error': 'Token expired'}), 401
      except Exception as e:
           return jsonify({'error': 'Token invalid', 'detail': str(e)}), 401
      return f(*args, **kwargs)
    return decorated
# GET /api/books?q=search
@api.route('/books', methods=['GET'])
def api_list_books():
   q = (request.args.get('q') or '').strip()
   if q:
    books = Book.query.filter((Book.title.ilike(f'%{q}%')) | (Book.author.ilike(f'%{q}%'))).all()
   else:
    books = Book.query.all()
   out = []
   for b in books:
     out.append({'id': b.id, 'title': b.title, 'author': b.author, 'description': b.description, 'stock': b.stock})
   return jsonify(out)
# POST /api/borrow {book_id}
@api.route('/borrow', methods=['POST'])
@token_required
def api_borrow():
   data = request.json or {}
   book_id = data.get('book_id')
   if not book_id:
      return jsonify({'error': 'book_id required'}), 400
   book = Book.query.get(book_id)
   if not book:
    return jsonify({'error': 'Book not found'}), 404
   if book.stock <= 0:
     return jsonify({'error': 'No stock available'}), 400
   user = request._jwt_user
   # create borrow
   borrow = Borrow(user_id=user.id, book_id=book.id)
   book.stock -= 1
   db.session.add(borrow)
   db.session.commit()
   return jsonify({'message': 'Book borrowed', 'borrow_id': borrow.id, 'book_stock': book.stock})
# POST /api/return {borrow_id}
@api.route('/return', methods=['POST'])
@token_required
def api_return():
  data = request.json or {}
  borrow_id = data.get('borrow_id')
  if not borrow_id:
    return jsonify({'error': 'borrow_id required'}), 400
  borrow = Borrow.query.get(borrow_id)
  if not borrow:
    return jsonify({'error': 'Borrow record not found'}), 404
  user = request._jwt_user
  if borrow.user_id != user.id:
     return jsonify({'error': 'Not authorized to return this borrow'}), 403
  if borrow.returned:
    return jsonify({'error': 'Already returned'}), 400
  borrow.returned = True
  borrow.returned_at = datetime.utcnow()
  borrow.book.stock += 1
  db.session.commit()
  return jsonify({'message': 'Book returned', 'book_stock': borrow.book.stock})
