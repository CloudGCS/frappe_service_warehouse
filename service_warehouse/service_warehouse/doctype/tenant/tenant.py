# Copyright (c) 2024, a-techsyn and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Tenant(Document):
	def validate(self):
		self.check_for_underscore("Tenant Code", self.tenant_code)
		self.check_for_underscore("Name", self.name)

	def before_rename(self, old_name, new_name, merge=False):
		self.check_for_underscore("Name", new_name)

	def check_for_underscore(self, field_name, value):
		if "_" in value:
			frappe.throw(_(f"{field_name} cannot contain underscore for doc: {self.name}"))

	def before_insert(self):
		if not frappe.db.exists("Service Provider", self.provider_code):
			provider = frappe.new_doc("Service Provider")
			provider.name = self.provider_code
			provider.title = self.provider_title
			provider.insert()
		self.service_provider = self.provider_code


@frappe.whitelist()
def get_session_tenant():
	if frappe.db.exists("Tenant", {"user": frappe.session.user}):
		return frappe.get_doc("Tenant", {"user": frappe.session.user})
	
	return None