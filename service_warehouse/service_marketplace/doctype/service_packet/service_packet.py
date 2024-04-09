# Copyright (c) 2024, a-techsyn and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document

from service_warehouse.service_warehouse.doctype.tenant.tenant import get_session_tenant

class ServicePacket(Document):
	def before_insert(self):
		tenant = get_session_tenant()
		if tenant:
			self.service_provider = tenant.service_provider
			if tenant.tenant_code == "HOST":
				self.is_system_packet = 1
		else:
			frappe.throw("You are not a tenant")

	def on_submit(self):
		if not self.latest_release:
				frappe.throw("Please set the latest release before submitting.")

	def subscribe(self):
		tenant = get_session_tenant()
		if tenant:
			service_subscription = frappe.new_doc("Service Subscription")
			service_subscription.service_packet = self.name
			service_subscription.tenant = tenant.name
			service_subscription.insert(ignore_permissions=True)
			subscriber = frappe.new_doc("Service Packet Subscription")
			subscriber.subscriber = service_subscription.name
			subscriber.parent = self.name
			subscriber.parenttype = "Service Packet"
			subscriber.parentfield = "subscriptions"
			subscriber.insert()
			# self.set("subscriptions", [subscriber])
			self.append("subscriptions", subscriber)
			self.save(ignore_permissions=True)
		else:
			frappe.throw("You are not a tenant")


@frappe.whitelist()
def subscribe(*args, **kwargs):
	service_packet = json.loads(kwargs.get('doc'))
	packet = frappe.get_doc("Service Packet", service_packet['name'])
	packet.subscribe()
	