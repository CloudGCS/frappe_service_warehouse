// Copyright (c) 2024, a-techsyn and contributors
// For license information, please see license.txt

frappe.ui.form.on("Service Packet", {
	before_submit: function(frm) {
    if (frm.doc.latest_release == null) {
      frappe.throw("You have no version of this packet. Please add a version before submitting."  );
      return false;
    }
  },
});
