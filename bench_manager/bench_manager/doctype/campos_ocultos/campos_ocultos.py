# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from bench_manager.api import set_conection
from bench_manager.bench_manager.utils import run_command
import datetime


class Camposocultos(Document):
    def before_save(self):
        frappe.db.commit()
        site = frappe.get_doc("Site", self.sitio)
        us = site.db_name
        pa = site.get_password('db_password')
        us, pa = set_conection(us, pa)

        for campo in self.campos:
            frappe.db.sql("""UPDATE `tabDocField` set hidden = {0}
                            WHERE parent = '{1}' and fieldname = '{2}'
                          """.format(campo.oculto, self.doctype_ex, campo.campo))
        frappe.db.commit()
        set_conection(us, pa)
        run_command(['bench --site {} clear-cache'.format(self.sitio)], self.doctype, unicode(datetime.datetime.now()), docname=self.name)
