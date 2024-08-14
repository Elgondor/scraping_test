from .extensions import db
from sqlalchemy.dialects.postgresql import UUID

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    uuid = db.Column(UUID(as_uuid=True), unique = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))


class PublicRegisterModel(db.Model):
    __tablename__ = "public_register_model"
    id = db.Column(db.Integer, primary_key = True)
    registrant = db.Column(db.String(50))
    public_register_status = db.Column(db.String(50))
    public_register_class = db.Column(db.String(50))
    practice_location = db.Column(db.String(500))


# These commented models are better related but because of the time I couldn't test them properly.

# class PublicRegisterModel(db.Model): 
#     __tablename__ = "public_register"
#     id = db.Column(db.Integer, primary_key = True)
#     registrant = db.Column(db.String(50))
#     # status = db.Column(db.String(50))
#     public_register_status_id = db.Column(db.Integer, db.ForeignKey('public_register_status.id'), unique=False, nullable=False)
#     # public_register_status = db.relationship("public_register_status", back_populates="public_register")
#     # data_class = db.Column(db.String(50))
#     public_register_class_id = db.Column(db.Integer, db.ForeignKey('public_register_class.id'), unique=False, nullable=False)
#     # public_register_class = db.relationship("public_register_class", back_populates="public_register")
#     practice_location = db.Column(db.String(500))

# class PublicRegisterStatusModel(db.Model): 
#     __tablename__ = "public_register_status"
#     id = db.Column(db.Integer, primary_key = True)
#     registration_status = db.Column(db.String(100))
#     public_registers = db.relationship('PublicRegisterModel', back_populates='public_register_status', lazy='dynamic')

# class PublicRegisterClassModel(db.Model):
#     __tablename__ = "public_register_class"
#     id = db.Column(db.Integer, primary_key = True)
#     registration_class = db.Column(db.String(100))
#     # public_registers = db.relationship('PublicRegisterModel', back_populates='public_register_class', lazy='dynamic')
