##-*-coding: utf-8;-*-##
from manager import Manager


def get_manager(db_url='sqlite:///:memory:', **more_config):
    return Manager(db_url)
