# Copyright (c) 2024, a-techsyn and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Tenant(Document):
	def before_insert(self):
		provider = frappe.new_doc("Service Provider")
		provider.title = self.provider_title
		provider.insert()
		self.service_provider = provider.name


@frappe.whitelist()
def get_session_tenant():
	tenant = frappe.get_doc("Tenant", {"user": frappe.session.user})
	return tenant