# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = ["Item Code:Link/Item:100","Colour:Link/Colour:100","Yard/Meter:Float:100","Group:Data:100",
		"In Qty:Float:100","Out Qty:Float:100","Document:Link/DocType:100","Document No:Dynamic Link/Document:100"]
	
	item_clause = ""
	if filters.get("item") :
		item_clause = """ AND ild.`item_code` """
	
	data = frappe.db.sql(""" 
		SELECT 

		il.`doctype_type`,
		il.`doctype_no`,
		il.`posting_date`,
		ild.`item_code_variant`,
		ild.`inventory_uom`,
		ild.`warehouse`,
		ild.`yard_atau_meter_per_roll`,
		ild.`qty_yard_atau_meter`,
		ild.`qty_roll`,
		ild.`colour` 

		FROM `tabInventory Ledger`il 
		JOIN `tabInventory Ledger Data`ild
		WHERE il.`is_cancelled`=0 
		AND il.`name` = ild.`parent` {0} {1} """.format(doctype_clause,date_clause),as_list=1)

	temp_data = []

	for i in data :
		if i[0] == "Packing List Receipt" :
			
			temp_data.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],0,0,i[9]])

		else :
			temp_data.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],0,0,i[7],i[8],i[9]])

	
	return columns, temp_data
