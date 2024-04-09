# Copyright (c) 2024, a-techsyn and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document

from frappe import _
from service_warehouse.service_warehouse.doctype.tenant.tenant import get_session_tenant

class ServiceExtension(Document):
	def validate(self):
		self.check_for_underscore("Name", self.name)
		self.check_for_underscore("Extension Code", self.extension_name)

	def before_rename(self, old_name, new_name, merge=False):
		self.check_for_underscore("Name", new_name)

	def check_for_underscore(self, field_name, value):
		if "_" in value:
			frappe.throw(_(f"{field_name} cannot contain underscore for doc: {self.name}"))

	
	def before_insert(self):
		tenant = get_session_tenant()
		if not tenant:
			frappe.throw("You are not a tenant")
		if not frappe.db.exists("Service Provider", tenant.service_provider):
			frappe.throw("You are not a valid tenant with well defined service provider.")		
		self.service_provider = tenant.service_provider

		if not self.is_version_valid():
			frappe.throw("Your version number should progress, can not be downgrading from the latest version created.")

	def is_version_valid(self):
		# self has major and minor version first retrive all the versions with same library name
		versions = frappe.get_all("Service Extension", 
														filters={"service_provider": self.service_provider, "extension_code": self.extension_code, "extension_type": self.extension_type}, 
														fields=["major", "minor"])
		if not versions:
			return True
		# check if the version is greater
		for version in versions:
			if version.major > self.major:
				return False
			elif version.major == self.major and version.minor >= self.minor:
				return False
		return True