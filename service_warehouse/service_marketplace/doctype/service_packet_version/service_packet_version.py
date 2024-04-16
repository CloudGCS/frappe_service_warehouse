# Copyright (c) 2024, a-techsyn and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from service_warehouse.service_warehouse.doctype.tenant.tenant import get_session_tenant

class ServicePacketVersion(Document):
	def before_insert(self):
		user = frappe.session.user
		if user == "Administrator" :
			return
		tenant = get_session_tenant()
		if tenant:
			is_valid_version = self.check_version()
			if not is_valid_version:
				frappe.throw("You are not allowed to add this version. Please check your major or minor values.")
		else:
			frappe.throw("You are not a tenant")

	def on_submit(self):
		service_packet = frappe.get_doc("Service Packet", self.service_packet)
		service_packet.latest_release = self.name
		service_packet.save()

	def check_version(self):
		# self has major and minor version first retrive all the versions with same library name
		versions = frappe.get_all("Service Packet Version", filters={"service_packet": self.service_packet}, fields=["major", "minor"])
		if not versions:
			return True
		# check if the version is greater
		for version in versions:
			if version.major > self.major:
				return False
			elif version.major == self.major and version.minor >= self.minor:
				return False
		return True
