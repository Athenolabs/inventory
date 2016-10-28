// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Laporan Reconciliasi"] = {
	"filters": [
		{
			"fieldname":"stock_recon",
			"label": __("Stock Reconciliation"),
			"fieldtype": "Link",
			"options": "Stock Reconciliation"
		},
		{
			"fieldname":"item",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item",
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
		},		
	]
}
