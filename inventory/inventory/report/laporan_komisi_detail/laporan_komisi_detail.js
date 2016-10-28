// Copyright (c) 2016, Myme and contributors
// For license information, please see license.txt

frappe.query_reports["Laporan Komisi Detail"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label":__("From :"),
			"fieldtype": "Date",
		},
		{
			"fieldname": "to_date",
			"label":__("To :"),
			"fieldtype": "Date",
		},
		{
			"fieldname": "sales_partner",
			"label":__("Sales Partner"),
			"fieldtype": "Link",
			"options": "Sales Partner"
		},
	]
}
