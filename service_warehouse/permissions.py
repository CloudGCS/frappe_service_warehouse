import frappe


def filter_service_packets(user):
  if not user:
    user = frappe.session.user

  tenant = frappe.get_doc("Tenant", {"user": user})  
  if tenant:
    # packets that belong to user or submitted by others
    return "(`tabService Packet`.owner = {user} or (`tabService Packet`.docstatus = 1 and `tabService Packet`.owner != {user}))".format(user=frappe.db.escape(user))
  else:
    return None
    