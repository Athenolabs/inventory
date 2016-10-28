// Copyright (c) 2016, Myme and contributors
// For license information, please see license.txt

frappe.query_reports["Inventory Ledger"] = {
	"filters": [
		/*
		{
			"fieldname": "from_date",
			"label":__("From"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "to_date",
			"label":__("To"),
			"fieldtype": "Date"
		},
		*/
		{
			"fieldname": "item",
			"label":__("Item Code"),
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname": "document",
			"label":__("Document"),
			"fieldtype": "Select",
			"options": "Packing List Receipt" + '\n'
				+ "Packing List Delivery" + '\n'
				+ "Stock Recon Inventory" + '\n'
				+ "Repack Inventory" 
		},
		{
			"fieldname": "document_no",
			"label":__("Document No"),
			"fieldtype": "Data"
		},
	]
}
