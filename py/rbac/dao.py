##-*-coding: utf-8;-*-##
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


RBAC_BASE = declarative_base()


class Role(RBAC_BASE):
    id_ = Column(BigInteger, autoincrement=True, primary_key=True)
    parent_id = Column(BigInteger, ForeignKey(id_))
    name = Column(String, unique=True)
    desc = Column(String)

    children = relationship('Role',
                            cascade='all,delete-orphan',
                            backref='parent'
    )


class User(RBAC_BASE):
    id_ = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(String, unique=True)
    desc = Column(String)
    active = Column(Boolean, default=False)


class Permission(RBAC_BASE):
    id_ = Column(BigInteger, autoincrement=True, primary_key=True)
    role_id = Column(BigInteger, ForeignKey(Role.id_))
    operation_id = Column(BigInteger, ForeignKey(Operation.id_))

    Role = relationship(Role)


class Operation(RBAC_BASE):
    id_ = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(String, unique=True)
    desc = Column(String)


class Session(RBAC_BASE):
    id_ = Column(BigInteger, autoincrement=True, primary_key=True)


class Constraints(RBAC_BASE):
    id_ = Column(BigInteger, autoincrement=True, primary_key=True)
