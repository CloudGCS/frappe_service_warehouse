# Copyright (c) 2024, a-techsyn and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document

from service_warehouse.service_warehouse.doctype.tenant.tenant import get_session_tenant

class ServiceExtension(Document):
	def before_insert(self):
		tenant = get_session_tenant()
		if tenant:
			self.service_provider = tenant.service_provider
			is_valid_version = self.check_version()
			if not is_valid_version:
				frappe.throw("You are not allowed to add this version. Please check your major or minor values.")
		else:
			frappe.throw("You are not a tenant")

	def check_version(self):
		# self has major and minor version first retrive all the versions with same library name
		versions = frappe.get_all("Service Extension", filters={"service_provider": self.service_provider, "library_name": self.library_name}, fields=["major", "minor"])
		if not versions:
			return True
		# check if the version is greater
		for version in versions:
			if version.major > self.major:
				return False
			elif version.major == self.major and version.minor >= self.minor:
				return False
		return True