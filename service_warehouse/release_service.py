import json

import frappe


@frappe.whitelist()
def check_update(*args, **kwargs):
	tenant_code = kwargs.get('tenant_code')

	# get service subscription filter by tenant
	service_packets = frappe.get_all("Service Subscription", fields=["service_packet"],
									 filters={"tenant_code": tenant_code})

	# get service package filter by service_packets
	service_packages = frappe.get_all("Service Packet", fields=["*"],
									  filters={"name": ["in", [packet.service_packet for packet in
															   service_packets]]})
	packages = []
	for service_package in service_packages:
		package = {
			"name": service_package.name,
			"title": service_package.title,
			"latest_release": service_package.latest_release,
			"service_provider": service_package.service_provider
		}
		packages.append(package)
	return packages


@frappe.whitelist()
def get_service_package(*args, **kwargs):
	input = json.loads(kwargs.get('input'))

	service_package = frappe.get_doc("Service Packet", "-".join(input.get('name').split("-")[:-1]))
	service_package_version = frappe.get_doc("Service Packet Version", input.get('name'))
	extensions = service_package_version.get("extensions")
	extension_docs = []
	for extension in extensions:
		extension_doc = frappe.get_doc("Service Extension",
									   "-".join(extension.get('name').split("-")[:-1]))
		extension_model = {
			"title": extension_doc.title,
			"library_name": extension_doc.library_name,
			"file_path": extension_doc.file,
			"major": extension_doc.major,
			"minor": extension_doc.minor,
			"extension_type": {
				"name": extension_doc.extension_type,
				"title": "extension_doc.extension_type_title"
			},
		}
		extension_docs.append(extension_model)

	return {
		'title': service_package.get('title'),
		'code_name': service_package.get('code_name'),
		'major': service_package_version.get('major'),
		'minor': service_package_version.get('minor'),
		'service_provider': {
			'name': service_package.get('service_provider'),
			'title': 'Provider 1'
		},
		'extensions': extension_docs
	}
	print("input: ", input)

