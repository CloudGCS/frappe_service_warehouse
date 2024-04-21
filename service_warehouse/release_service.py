import json
import frappe


@frappe.whitelist()
def check_update(tenant_code):
	
	# get service subscription filter by tenant
	service_packets = frappe.get_all("Service Subscription", fields=["service_packet"],
									 filters={"tenant": tenant_code})

	# get service package filter by service_packets
	service_packages = frappe.get_all("Service Packet", fields=["*"],
									  filters={"name": ["in", [packet.service_packet for packet in
															   service_packets]]})
	packages = []
	for service_package in service_packages:
		package = {
			"name": service_package.name,
			"title": service_package.title,
			"release_version": service_package.latest_release,
			"service_provider": service_package.service_provider
		}
		packages.append(package)
	return packages


@frappe.whitelist()
def get_service_package(packet_release_version):
	
	packet_name = "_".join(packet_release_version.split("_")[:-1])

	service_package = frappe.get_doc("Service Packet", packet_name)
	service_package_version = frappe.get_doc("Service Packet Version", packet_release_version)
	packet_service_provider = frappe.get_doc("Service Provider", service_package.get('service_provider'))
	extensions = service_package_version.get("extensions")
	extension_docs = []
	extension_type_cache = {}
	for extension in extensions:
		extension_doc = frappe.get_doc("Service Extension",
									   "_".join(extension.get('name').split("_")[:-1]))
		if extension_doc.extension_type not in extension_type_cache:
			extension_type_cache[extension_doc.extension_type] = frappe.get_doc("Service Extension Type", extension_doc.extension_type, fields=["name", "title"])
		extension_type_doc = extension_type_cache[extension_doc.extension_type]
		extension_model = {
			"title": extension_doc.title,
			"library_name": extension_doc.library_name,
			"file_path": extension_doc.file,
			"major": extension_doc.major,
			"minor": extension_doc.minor,
			"extension_type": {
				"name": extension_doc.extension_type,
				"title": extension_type_doc.title
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
			'title': packet_service_provider.title
		},
		'extensions': extension_docs
	}

