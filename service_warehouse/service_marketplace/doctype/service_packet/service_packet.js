// Copyright (c) 2024, a-techsyn and contributors
// For license information, please see license.txt

frappe.ui.form.on("Service Packet", {
	onload: async function(frm) {
    var subscription_possible = frm.doc.docStatus != 1
    subscription_possible = subscription_possible && frm.doc.service_provider != null

    const response = await frappe.call({
      method: "service_warehouse.service_warehouse.doctype.tenant.tenant.get_session_tenant",
      args: {}
    });
    debugger
    var tenant = response.message;
    subscription_possible = subscription_possible && tenant != null && tenant.service_provider != frm.doc.service_provider
    subscription_possible = subscription_possible && frm.doc.subscriptions.filter(sub => sub.tenant == tenant.name).length == 0
    frm.set_df_property('subscribe', 'hidden', !subscription_possible);
  },
  before_submit: function(frm) {
    if (frm.doc.latest_release == null) {
      frappe.throw("You have no version of this packet. Please add a version before submitting."  );
      return false;
    }
  },
  subscribe: function(frm){
    frappe.call({
      method: "service_warehouse.service_marketplace.doctype.service_packet.service_packet.subscribe",
      args: {
        doc: frm.doc,
      },
      freeze: true,
      callback: function (r) {
        frappe.msgprint("Subscription successful. You can now use this packet.");
        frm.reload_doc();
      },
      error: (r) => {
        frappe.msgprint("Something went wrong, please try again later\n" + r.message);
      }
    });
  }
});
