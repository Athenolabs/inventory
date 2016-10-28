# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	
	columns = []
	select_field = ""
	group_clause = ""
	order_clause = ""
	left_join = ""
	if filters.get("group_by") == "Customer" :
		columns = ["Customer:Link/Customer:100","Item Code:Link/Item:100","Colour:Data:100","Qty Pending Order:Float:150","Qty Sisa di Pending Order:Float:200",
			"Qty Teralokasi:Float:150"]
		select_field = " po.`customer`,por.`item_code_roll`,por.`colour`,por.`roll_qty`,por.`qty_sisa`,por.`qty_dialokasi` "
		order_clause = " ORDER BY po.`customer` "
	elif filters.get("group_by") == "Item" :
		columns = ["Item Code:Link/Item:100","Colour:Data:100","Qty Pending Order:Float:150","Qty Sisa di Pending Order:Float:200",
			"Qty Teralokasi:Float:150"]
		select_field = " por.`item_code_roll`,por.`colour`,por.`roll_qty`,por.`qty_sisa`,por.`qty_dialokasi` "
		iorder_clause = " ORDER BY por.`item_code_roll` "
	elif filters.get("group_by") == "Colour":
		columns = ["Colour:Data:100","Item Code:Link/Item:100","Qty Pending Order:Float:150","Qty Sisa di Pending Order:Float:200",
			"Qty Teralokasi:Float:150"]
		select_field = " por.`colour`,por.`item_code_roll`,por.`roll_qty`,por.`qty_sisa`,por.`qty_dialokasi` "
		order_clause = " ORDER BY por.`colour` "
	elif filters.get("group_by") == "Pending Order" :
		columns = ["Pending Order No.:Link/Pending Order:100","Item Code:Link/Item:100","Colour:Data:100","Qty Pending Order:Float:150","Qty Sisa di Pending Order:Float:200",
			"Alokasi No.:Link/Alokasi Barang:100","Qty Alokasi:Float:100"]
		select_field = " po.`name`,por.`item_code_roll`,por.`colour`,por.`roll_qty`,por.`qty_sisa`,ab.`name`,abd.`roll_qty` "
		left_join = """ LEFT JOIN `tabAlokasi Barang`ab ON ab.`pending_order`=po.`name` AND ab.`docstatus`=1
			LEFT JOIN `tabAlokasi Barang Data`abd ON ab.`name`=abd.`parent` 
			AND abd.`item_code_roll`=por.`item_code_roll` AND abd.`colour`=por.`colour`  """
		order_clause = " ORDER BY po.`name` "
	else :
		return [],[]
	
	po_clause = ""
	if filters.get("pending_order") :
		po_clause = """ AND po.`name`="{0}" """.format(filters.get("pending_order"))
	
	item_clause = ""
	if filters.get("item") :
		item_clause = """ AND por.`item_code_roll`="{0}" """.format(filters.get("item"))
	
	customer_clause = ""
	if filters.get("customer") :
		customer_clause = """ AND po.`customer`="{0}" """.format(filters.get("customer"))
	
	colour_clause = ""
	if filters.get("colour") :
		colour_clause = """ AND por.`colour`="{0}" """.format(filters.get("colour"))
	
	
	delivery_clause = ""
	if filters.get("delivery_from_date") and filters.get("delivery_to_date"):
		delivery_clause = """ AND po.`expected_delivery_date` BETWEEN "{0}" AND "{1}" """.format(filters.get("delivery_from_date"),filters.get("delivery_to_date"))
	
	date_clause = ""
	if filters.get("posting_from_date") and filters.get("posting_to_date"):
		delivery_clause = """ AND po.`posting_date` BETWEEN "{0}" AND "{1}" """.format(filters.get("posting_from_date"),filters.get("posting_to_date"))
	
	data = frappe.db.sql(""" SELECT {0}
		FROM `tabPending Order`po 
		JOIN `tabPending Order Roll`por ON por.`parent`=po.`name`
		{1}
		WHERE po.`docstatus`=1
		{2} {3} {4} {5} {6} {7}
		{8} """.format(select_field,left_join,po_clause,item_clause,customer_clause,colour_clause,delivery_clause,date_clause,order_clause))
	
	return columns, data
