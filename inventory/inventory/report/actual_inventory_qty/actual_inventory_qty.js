// Copyright (c) 2016, Myme and contributors
// For license information, please see license.txt

frappe.query_reports["Actual Inventory Qty"] = {
	"filters": [
		{
			"fieldname": "item",
			"label":__("Item"),
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname": "colour",
			"label":__("Colour"),
			"fieldtype": "Link",
			"options": "Colour"
		},
		{
			"fieldname": "group",
			"label":__("Group"),
			"fieldtype": "Data",
		},
		{
			"fieldname": "is_negative",
			"label":__("Negative Only"),
			"fieldtype": "Check",
		},
	]
}
