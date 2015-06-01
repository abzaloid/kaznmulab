# coding=utf-8

import logging

from google.appengine.ext import db
from google.appengine.api import memcache

import models
import pickle

def store(key, value, chunksize=950000):
    serialized = pickle.dumps(value, 2)
    values = {}
    for i in xrange(0, len(serialized), chunksize):
        values['%s.%s' % (key, i//chunksize)] = serialized[i : i+chunksize]
    return memcache.set_multi(values)

def retrieve(key):
    result = memcache.get_multi(['%s.%s' % (key, i) for i in xrange(32)])
    if result:
        serialized_data = ''.join([i for key, i in sorted(result.items()) if key in result and i is not None])
        return pickle.loads(serialized_data)
    else:
        return None

### CACHING ###

def get_bi(update = False):
    key = "my_bi"
    items = retrieve(key)
    if items is None or update:
        items = list(db.GqlQuery("SELECT * FROM BI"))
        store(key, items)
    return items

def get_bik(update = False):
    key = "my_bik"
    items = retrieve(key)
    if items is None or update:
        items = list(db.GqlQuery("SELECT * FROM BIK"))
        store(key, items)
    return items

def get_oik(update = False):
    key = "my_oik"
    items = retrieve(key)
    if items is None or update:
        items = list(db.GqlQuery("SELECT * FROM OIK"))
        store(key, items)
    return items

def get_isg(update = False):
    key = "my_isg"
    items = retrieve(key)
    if items is None or update:
        items = list(db.GqlQuery("SELECT * FROM ISG"))
        store(key, items)
    return items

def get_diz(update = False):
    key = "my_diz"
    items = retrieve(key)
    if items is None or update:
        items = list(db.GqlQuery("SELECT * FROM DIZ"))
        store(key, items)
    return items


def get_all(update = False):
    key = "my_all"
    items = retrieve(key)
    if items is None or update:
        items = []
        items = get_bi() + get_diz() + get_isg() + get_oik() + get_bik()
        store(key, items)
    return items
