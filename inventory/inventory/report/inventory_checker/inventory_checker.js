// Copyright (c) 2016, Myme and contributors
// For license information, please see license.txt

frappe.query_reports["Inventory Checker"] = {
	"filters": [
		{
			"fieldname": "inventory_validator",
			"label":__("Inventory Validator"),
			"fieldtype": "Link",
			"options" : "Inventory Validator",
			"reqd" : 1,
		},
	]
}
