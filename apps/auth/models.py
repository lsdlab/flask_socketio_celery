import datetime as dt
from flask_login import UserMixin

from apps.database import (Column, Model, SurrogatePK, db,
                           reference_col, relationship)
from apps.extensions import bcrypt


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'auth_roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('auth_users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'auth_users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=True)
    #: The hashed password
    password = Column(db.Binary(128), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    sid = Column(db.String(80), nullable=True, default='')

    def __init__(self, username, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'active': self.active,
            'is_admin': self.is_admin,
            'sid': self.sid,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
