# coding=utf-8

from google.appengine.ext import db


### MODELS ###
class BI(db.Model):
    name = db.StringProperty()
    category = db.StringProperty()
    price = db.StringProperty()
    parentt = db.StringProperty()

class BIK(db.Model):
    name = db.StringProperty()
    category = db.StringProperty()
    price = db.StringProperty()
    parentt = db.StringProperty()


class DIZ(db.Model):
    name = db.StringProperty()
    category = db.StringProperty()
    price = db.StringProperty()
    parentt = db.StringProperty()

class ISG(db.Model):
    name = db.StringProperty()
    category = db.StringProperty()
    price = db.StringProperty()
    parentt = db.StringProperty()

class OIK(db.Model):
    name = db.StringProperty()
    category = db.StringProperty()
    parentt = db.StringProperty()
    price = db.StringProperty()