##-*-coding: utf-8;-*-##
import contextlib
import functools

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dao import RBAC_BASE
from dao import User
from dao import Role
from dao import Operation


@contextlib.contextmanager
def session(session_factory):
    s = session_factory()

    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()


def service(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kargs):
        with session(self.Session) as s:
            return func(self, s, *args, **kargs)

    return wrapper


class Manager(object):
    def __init__(self, db_url, **more_config):
        self.db_url = db_url
        self.engine = create_engine(self.db_url, pool_recycle=3600, echo=True)
        self.Session = sessionmaker(bind=self.engine)
        RBAC_BASE.metadata.create_all(self.engine)


    @service
    def add_user(self, s, name, desc=None, active=False):
        s.add(User(name=name, desc=desc, active=active))


    @service
    def remove_user(self, s, name):
        u = s.query(User).filter_by(name=name).one_or_none()
        s.delete(u)


    @service
    def activate_user(self, s, name):
        s.query(User).filter_by(name=name).update({User.active: True})


    @service
    def deactivate_user(self, s, name):
        s.query(User).filter_by(name=name).update({User.active: False})


    @service
    def describe_user(self, s, name, desc):
        s.query(User).filter_by(name=name).update({User.desc: desc})


    @service
    def find_user(self, s, name):
        u = s.query(User).filter_by(name=name).one_or_none()
        if u is None:
            return None

        return {
            'name': u.name,
            'desc': u.desc,
            'active': u.active
        }


    @service
    def add_role(self, s, name, desc=None, parent=None):
        c = Role(name=name, desc=desc)
        s.add(c)

        if parent is None:
            return

        p = s.query(Role).filter_by(name=parent).one_or_none()
        c.inherit(p)


    @service
    def remove_role(self, s, name):
        r = s.query(Role).filter_by(name=name).one_or_none()
        s.delete(r)


    @service
    def describe_role(self, s, name, desc):
        s.query(Role).filter_by(name=name).update({Role.desc: desc})


    @service
    def find_role(self, s, name):
        r = s.query(Role).filter_by(name=name).one_or_none()
        if r is None:
            return None

        return {
            'name': r.name,
            'desc': r.desc
        }


    @service
    def inherit_role(self, s, child, parent):
        c = s.query(Role).filter_by(name=child).one_or_none()
        p = s.query(Role).filter_by(name=parent).one_or_none()
        c.inherit(p)


    @service
    def add_operation(self, s, name, desc=None):
        s.add(Operation(name=name, desc=desc))


    @service
    def remove_operation(self, s, name):
        op = s.query(Operation).filter_by(name=name).one_or_none()
        s.delete(op)


    @service
    def describe_operation(self, s, name, desc):
        s.query(Operation).filter_by(name=name).update({Operation.desc: desc})


    @service
    def find_operation(self, s, name):
        op = s.query(Operation).filter_by(name=name).one_or_none()
        if op is None:
            return None

        return {
            'name': op.name,
            'desc': op.desc
        }


    @service
    def assign_user_to_role(self, s, user, role):
        u = s.query(User).filter_by(name=user).one_or_none()
        r = s.query(Role).filter_by(name=role).one_or_none()
        u.assign(r)


    @service
    def remove_user_from_role(self, s, user, role):
        u = s.query(User).filter_by(name=user).one_or_none()
        r = s.query(Role).filter_by(name=role).one_or_none()
        u.resign(r)


    @service
    def assign_operation_to_role(self, s, operation, role):
        op = s.query(Operation).filter_by(name=operation).one_or_none()
        r = s.query(Role).filter_by(name=role).one_or_none()
        op.assign(r)


    @service
    def revoke_operation_from_role(self, s, operation, role):
        op = s.query(Operation).filter_by(name=operation).one_or_none()
        r = s.query(Role).filter_by(name=role).one_or_none()
        op.revoke(r)


    @service
    def permitted(self, s, user, operation):
        u = s.query(User).filter_by(name=user).one_or_none()
        if u is None:
            return False

        return u.can(operation)
