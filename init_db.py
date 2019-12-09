# -*- coding: utf-8 -*-
from flaski.app import db
import os


os.remove("./flaski/test.db")
db.create_all()
