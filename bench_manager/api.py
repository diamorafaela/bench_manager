import frappe


def set_conection(user, password):
    pa = frappe.db.password
    us = frappe.db.user
    frappe.db.user = user
    frappe.db.password = password
    frappe.db.connect()
    return us, pa


@frappe.whitelist()
def get_site_docs(site):
    site = frappe.get_doc("Site", site)
    us = site.db_name
    pa = site.get_password('db_password')
    us, pa = set_conection(us, pa)

    lista = frappe.db.sql("""SELECT distinct parent from `tabDocField`""")
    set_conection(us, pa)
    return "".join(["\n{}".format(t[0]) for t in lista])


@frappe.whitelist()
def get_campos_doc(site, doc):
    site = frappe.get_doc("Site", site)
    us = site.db_name
    pa = site.get_password('db_password')
    us, pa = set_conection(us, pa)

    lista = frappe.db.sql("""SELECT distinct fieldname from `tabDocField` where parent='{}'""".format(doc))
    set_conection(us, pa)
    return "".join(["\n{}".format(t[0]) for t in lista])


@frappe.whitelist()
def get_hidden(site, doc, campo):
    site = frappe.get_doc("Site", site)
    us = site.db_name
    pa = site.get_password('db_password')
    us, pa = set_conection(us, pa)

    lista = frappe.db.sql("""SELECT hidden from `tabDocField` where parent='{0}' and fieldname = '{1}'""".format(doc, campo))
    set_conection(us, pa)
    if lista:
        return lista[0][0]
    return 0
