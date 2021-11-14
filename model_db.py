# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 10:35:20 2021

@author: Smegn
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import bcrypt

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    token = db.Column(db.String(36), unique=True)
    password = db.Column(db.Text)
    is_admin = db.Column(db.Boolean)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    @property
    def email(self):
        return f"{self.first_name}.{self.last_name}@tudublin.ie"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.name

    @staticmethod
    def create_password_hash(plaintext_password):
        if not plaintext_password:
            return None
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(b'plaintext_password', salt)

    def password_is_verified(self, entered_password):
        return bcrypt.checkpw(b'entered_password', self.password)



class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    hashtag = db.Column(db.String(20))
    description = db.Column(db.Text)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __str__(self):
        return f"{self.name} (#{self.hashtag})"


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    title = db.Column(db.String(50))
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    content = db.Column(db.Text)
    owner = db.relationship(User, backref=db.backref("owner_assoc"))
    category = db.relationship(Category, backref=db.backref("category_assoc"))

    def __str__(self):
        return f"{self.title}"