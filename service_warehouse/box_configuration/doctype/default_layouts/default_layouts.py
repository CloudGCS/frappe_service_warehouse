# Copyright (c) 2024, CloudGCS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DefaultLayouts(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		layout: DF.JSON
		platform: DF.Literal["Desktop", "Mobile"]
		source: DF.Literal["Default", "Tenant"]
		viewer: DF.Literal["Pilot", "Observer", "Test"]
	# end: auto-generated types
	pass

@frappe.whitelist()
def get_default_layouts():
	default_layouts = frappe.get_all("Default Layouts",fields=["name","platform","viewer","source","layout"] ,filters={"source": "Default"})
	return default_layouts


