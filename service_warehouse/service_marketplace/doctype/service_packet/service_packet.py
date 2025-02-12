# Copyright (c) 2024, a-techsyn and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from frappe import _

from service_warehouse.service_warehouse.doctype.tenant.tenant import get_host_user, get_session_tenant

class ServicePacket(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		code_name: DF.Data
		description: DF.Text | None
		is_seed_data: DF.Check
		is_system_packet: DF.Check
		latest_release: DF.Link | None
		service_provider: DF.Link | None
		title: DF.Data
	# end: auto-generated types

	def validate(self):
		self.check_for_underscore("Packet Code", self.code_name)

	def check_for_underscore(self, field_name, value):
		if "_" in value:
			frappe.throw(_(f"{field_name} cannot contain underscore for doc: {self.name}"))

	def before_insert(self):
		if self.is_seed_data:
			return
		tenant = get_session_tenant()
		if not tenant:
			frappe.throw("You are not a tenant")

		if not frappe.db.exists("Service Provider", tenant.service_provider):
			frappe.throw("You are not a valid tenant with well defined service provider.")		
		self.service_provider = tenant.service_provider

		if tenant.tenant_code == "HOST":
			self.is_system_packet = 1
	
	def after_insert(self):
		if self.is_seed_data:
			self.owner = get_host_user()
			frappe.db.set_value("Service Packet", self.name, "owner", get_host_user())

	def on_submit(self):
		if not self.latest_release:
				frappe.throw("Please set the latest release before submitting.")

	def subscribe(self, tenant):
		
		if not tenant:
			frappe.throw("tenant is required to subscribe to a service packet.")

		# check for existing subscription with tenant and packet
		tenants_subscriptions = frappe.db.exists("Service Subscription", {"tenant": tenant.name, "service_packet": self.name})
		if tenants_subscriptions:
			frappe.throw("You are already subscribed to this service packet.")

		service_subscription = frappe.new_doc("Service Subscription")
		service_subscription.service_packet = self.name
		service_subscription.tenant = tenant.name
		service_subscription.insert(ignore_permissions=True)
		

# this method should be called on DocType Service Packet only.
@frappe.whitelist()
def subscribe(*args, **kwargs):
	service_packet = json.loads(kwargs.get('doc'))
	packet = frappe.get_doc("Service Packet", service_packet['name'])
	tenant = get_session_tenant()
	if not tenant:
		frappe.throw("You are not a tenant - you are not allowed to subscribe to this service packet.")
	packet.subscribe(tenant)
	