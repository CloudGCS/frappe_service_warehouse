# Copyright (c) 2024, a-techsyn and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from frappe import _

from service_warehouse.service_warehouse.doctype.tenant.tenant import get_host_user, get_session_tenant

class ServicePacket(Document):
	def validate(self):
		self.check_for_underscore("Packet Code", self.code_name)

	def check_for_underscore(self, field_name, value):
		if "_" in value:
			frappe.throw(_(f"{field_name} cannot contain underscore for doc: {self.name}"))

	def before_insert(self):
		user = frappe.session.user
		# todo: we need to make a better check for fixtures - this is a temporary fix
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
			# link to existing subscriptions
			subscriptions = frappe.get_all("Service Subscription", filters={"service_packet": self.name})
			for subscription in subscriptions:
				self.create_packet_subscription(subscription)

	def on_submit(self):
		if not self.latest_release:
				frappe.throw("Please set the latest release before submitting.")

	def create_packet_subscription(self, service_subscription):
		subscriber = frappe.new_doc("Service Packet Subscription")
		subscriber.parent = self.name
		subscriber.parenttype = "Service Packet"
		subscriber.parentfield = "subscriptions"
		subscriber.subscriber = service_subscription.name
		subscriber.insert()
		return subscriber

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
		subscriber = self.create_packet_subscription(service_subscription)
		
		self.append("subscriptions", subscriber)
		self.save(ignore_permissions=True)
		

# this method should be called on DocType Service Packet only.
@frappe.whitelist()
def subscribe(*args, **kwargs):
	service_packet = json.loads(kwargs.get('doc'))
	packet = frappe.get_doc("Service Packet", service_packet['name'])
	tenant = get_session_tenant()
	if not tenant:
		frappe.throw("You are not a tenant - you are not allowed to subscribe to this service packet.")
	packet.subscribe(tenant)
	