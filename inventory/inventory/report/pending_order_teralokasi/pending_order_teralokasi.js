// Copyright (c) 2016, Myme and contributors
// For license information, please see license.txt

frappe.query_reports["Pending Order Teralokasi"] = {
	"filters": [
		{
			"fieldname": "group_by",
			"label":__("Group By"),
			"fieldtype": "Select",
			"options": "Customer" + '\n'
				+ "Item" + '\n'
				+ "Colour" + '\n'
				+ "Pending Order",
			"reqd":1
		},
		{
			"fieldname": "pending_order",
			"label":__("Pending Order No."),
			"fieldtype": "Link",
			"options": "Pending Order"
		},
		{
			"fieldname": "item",
			"label":__("Item"),
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname": "customer",
			"label":__("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "colour",
			"label":__("Colour"),
			"fieldtype": "Link",
			"options": "Colour"
		},
		{
			"fieldname": "delivery_from_date",
			"label":__("Expected Delivery Date From"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "delivery_to_date",
			"label":__("Expected Delivery Date To"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "posting_from_date",
			"label":__("Posting Date From"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "posting_to_date",
			"label":__("Posting Date To"),
			"fieldtype": "Date"
		},
		
	]
}
