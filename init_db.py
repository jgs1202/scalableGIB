# -*- coding: utf-8 -*-
from flaski.app import db
import os

try:
    os.remove("./flaski/test.db")
except:
    pass
db.create_all()
