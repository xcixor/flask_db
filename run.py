
"""Runs this app"""
from flask_sqlalchemy import SQLAlchemy

from flask import Flask

import os

from flask_script import Shell, Manager

from flask_migrate import Migrate, MigrateCommand

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
db = SQLAlchemy(app)
#eeps track of changes to a database schema, and then incremental changes
#can be applied to the database
migrate = Migrate(app, db)




class User(db.Model):
    """Defines the user table"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True)
    shopping_lists = db.relationship('ShoppingList', backref = 'owner', lazy='dynamic')

    def __repr__(self):
        return "[Id: {0.id}, Name: {0.name}]".format(self)
   
class ShoppingList(db.Model):
    """Defines shopping lists"""
    __tablename__ = 'shopping_lists'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "[Id: {0.id}, Name: {0.name}, Owner: {0.user_id}]".format(self) 
class ShoppingListItem(db.Model):
    """Defines a shopping list item"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    quantity =db.Column(db.Integer, default=1)
    price = db.Column(db.Integer, default=100)

    def __repr__(self):
        return "Id: {0.id}, Name: {0.name}, Quantity: {0.quantity}, Price: {0.price}".format(self)

def make_shell_context():
    return dict(app=app, db=db, User=User, ShoppingList=ShoppingList)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()