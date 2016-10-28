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
		columns = ["Customer:Link/Customer:100","Item Code:Link/Item:100","Colour:Data:100","Yard/Meter per Roll:Float:150","Qty Pending Order:Float:150","Qty Sisa di Pending Order:Float:200",
			"Qty Terkirim:Float:150"]
		select_field = " ab.`customer`,abd.`item_code_roll`,abd.`colour`,abd.`yard_atau_meter_per_roll`,abd.`roll_qty`,abd.`qty_sisa`,abd.`qty_terkirim` "
		order_clause = " ORDER BY ab.`customer` "
	elif filters.get("group_by") == "Item" :
		columns = ["Item Code:Link/Item:100","Colour:Data:100","Yard/Meter per Roll:Float:150","Qty Pending Order:Float:150","Qty Sisa di Pending Order:Float:200",
			"Qty Terkirim:Float:150"]
		select_field = " abd.`item_code_roll`,abd.`colour`,abd.`yard_atau_meter_per_roll`,abd.`roll_qty`,abd.`qty_sisa`,abd.`qty_terkirim` "
		iorder_clause = " ORDER BY abd.`item_code_roll` "
	elif filters.get("group_by") == "Colour":
		columns = ["Colour:Data:100","Item Code:Link/Item:100","Yard/Meter per Roll:Float:150","Qty Pending Order:Float:150","Qty Sisa di Pending Order:Float:200",
			"Qty Terkirim:Float:150"]
		select_field = " abd.`colour`,abd.`item_code_roll`,abd.`yard_atau_meter_per_roll`,abd.`roll_qty`,abd.`qty_sisa`,abd.`qty_terkirim` "
		order_clause = " ORDER BY abd.`colour` "
	elif filters.get("group_by") == "Alokasi Barang" :
		columns = ["Alokasi Barang No.:Link/Alokasi Barang:100","Item Code:Link/Item:100","Colour:Data:100","Yard/Meter per Roll:Float:150","Qty Pending Order:Float:150","Qty Sisa di Pending Order:Float:200",
			"Alokasi No.:Link/Alokasi Barang:100","Qty Delivery:Float:100"]
		select_field = " ab.`name`,abd.`item_code_roll`,abd.`colour`,abd.`yard_atau_meter_per_roll`,abd.`roll_qty`,abd.`qty_sisa`,pld.`name`,pldd.`roll_qty` "
		left_join = """ LEFT JOIN `tabPacking List Delivery`pld ON pld.`alokasi_barang`=ab.`name` AND pld.`docstatus`=1
			LEFT JOIN `tabPacking List Delivery Data`pldd ON pld.`name`=pldd.`parent` 
			AND pldd.`item_code_roll`=abd.`item_code_roll` AND pldd.`colour`=abd.`colour` AND pldd.`yard_atau_meter_per_roll`=abd.`yard_atau_meter_per_roll` 
			AND pldd.`group`=abd.`group`
			"""
		order_clause = " ORDER BY ab.`name` "
	else :
		return [],[]
	
	ab_clause = ""
	if filters.get("alokasi_barang") :
		ab_clause = """ AND ab.`name`="{0}" """.format(filters.get("alokasi_barang"))
	
	item_clause = ""
	if filters.get("item") :
		item_clause = """ AND abd.`item_code_roll`="{0}" """.format(filters.get("item"))
	
	customer_clause = ""
	if filters.get("customer") :
		customer_clause = """ AND ab.`customer`="{0}" """.format(filters.get("customer"))
	
	colour_clause = ""
	if filters.get("colour") :
		colour_clause = """ AND abd.`colour`="{0}" """.format(filters.get("colour"))
	
	
	delivery_clause = ""
	if filters.get("delivery_from_date") and filters.get("delivery_to_date"):
		delivery_clause = """ AND ab.`expected_delivery_date` BETWEEN "{0}" AND "{1}" """.format(filters.get("delivery_from_date"),filters.get("delivery_to_date"))
	
	date_clause = ""
	if filters.get("posting_from_date") and filters.get("posting_to_date"):
		delivery_clause = """ AND ab.`posting_date` BETWEEN "{0}" AND "{1}" """.format(filters.get("posting_from_date"),filters.get("posting_to_date"))
	
	data = frappe.db.sql(""" SELECT {0}
		FROM `tabAlokasi Barang`ab 
		JOIN `tabAlokasi Barang Data`abd ON abd.`parent`=ab.`name`
		{1}
		WHERE ab.`docstatus`=1
		{2} {3} {4} {5} {6} {7}
		{8} """.format(select_field,left_join,ab_clause,item_clause,customer_clause,colour_clause,delivery_clause,date_clause,order_clause))
	
	return columns, data
