// Copyright (c) 2024, a-techsyn and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Tenant", {
// 	refresh(frm) {

// 	},
// });

// frappe.form.link_formatters['Service Provider'] = function(value, doc) {
//   debugger
//   return doc.title
// }

frappe.ui.form.on('Tenant', {
  onload: function(frm) {
      if (frm.is_new()) {
          frm.set_df_property('provider_title', 'hidden', false);
      } else {
          frm.set_df_property('provider_title', 'hidden', true);
      }
  }
});