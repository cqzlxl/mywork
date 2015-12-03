##-*-coding: utf-8;-*-##
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import config


RBAC_BASE = declarative_base(name=config.declarative_basename)


class User(RBAC_BASE):
    __tablename__ = 'rbac_users'

    id_ = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(String(255), unique=True)
    desc = Column(String(255))
    active = Column(Boolean, default=False)


    def can(self, op):
        return any(r.can(op) for r in self.roles)


    def assign(self, role):
        self.roles.append(role)


class Role(RBAC_BASE):
    __tablename__ = 'rbac_roles'

    id_ = Column(BigInteger, autoincrement=True, primary_key=True)
    parent_id = Column(BigInteger, ForeignKey(id_))
    name = Column(String(255), unique=True)
    desc = Column(String(255))

    parent = relationship('Role',
                          cascade='all,delete-orphan',
                          remote_side=[id_],
                          single_parent=True,
                          backref='children'
    )

    users = relationship('User',
                         cascade='all',
                         secondary=lambda: UserRole.__table__,
                         backref='roles'
    )

    operations = relationship('Operation',
                              cascade='all',
                              secondary=lambda: RoleOperation.__table__,
                              backref='roles'
    )


    def can(self, op):
        for e in self.operations:
            if op == e.name:
                return True
        else:
            return False


    def assign(self, operation):
        self.operations.append(operation)


class Operation(RBAC_BASE):
    __tablename__ = 'rbac_operations'

    id_ = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(String(255), unique=True)
    desc = Column(String(255))


class UserRole(RBAC_BASE):
    __tablename__ = 'rbac_user_role'

    id_ = Column(BigInteger, autoincrement=True, primary_key=True)
    user_id = Column(BigInteger, ForeignKey(User.id_))
    role_id = Column(BigInteger, ForeignKey(Role.id_))

    UniqueConstraint(user_id, role_id)


class RoleOperation(RBAC_BASE):
    __tablename__ = 'rbac_role_operation'

    id_ = Column(BigInteger, autoincrement=True, primary_key=True)
    role_id = Column(BigInteger, ForeignKey(Role.id_))
    operation_id = Column(BigInteger, ForeignKey(Operation.id_))

    UniqueConstraint(role_id, operation_id)


'''
class Session(RBAC_BASE):
    pass


class Constraints(RBAC_BASE):
    pass
'''
