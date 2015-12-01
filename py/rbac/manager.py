##-*-coding: utf-8;-*-##
import sqlalchemy


def get_manager(db_url='sqlite:///:memory:', tab_prefix='rbac_', **more_config):
    engine = sqlalchemy.create_engine(db_url)
