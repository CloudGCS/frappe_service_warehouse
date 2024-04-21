# Copyright (c) 2024, a-techsyn and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


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

	def after_insert(self):
		if self.tenant_code != "HOST":
			# get service packets with is_system_packet = 1
			service_packets = frappe.get_all("Service Packet", filters={"is_system_packet": 1})
			for packet in service_packets:
				packet_doc = frappe.get_doc("Service Packet", packet.name)
				packet_doc.subscribe(self)


@frappe.whitelist()
def get_session_tenant():
	if frappe.db.exists("Tenant", {"user": frappe.session.user}):
		return frappe.get_doc("Tenant", {"user": frappe.session.user})
	
	return None

def get_host_user():
	return frappe.get_doc("Tenant", "HOST").user