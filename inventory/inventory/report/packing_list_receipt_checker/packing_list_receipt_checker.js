// Copyright (c) 2016, Myme and contributors
// For license information, please see license.txt

frappe.query_reports["Packing List Receipt Checker"] = {
	"filters": [
		{
			"fieldname": "packing_list_receipt",
			"label":__("Packing List Receipt"),
			"fieldtype": "Link",
			"options" : "Packing List Receipt",
			"reqd" : 1,
		},
	]
}
