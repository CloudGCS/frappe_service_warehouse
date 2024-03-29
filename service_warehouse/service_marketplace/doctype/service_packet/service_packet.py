# Copyright (c) 2024, a-techsyn and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from service_warehouse.service_warehouse.doctype.tenant.tenant import get_session_tenant

class ServicePacket(Document):
	def before_insert(self):
		tenant = get_session_tenant()
		if tenant:
			self.service_provider = tenant.service_provider
		else:
			frappe.throw("You are not a tenant")
