# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	
	columns = ["Produk:Link/Item:100","Tanggal Rekonsiliasi:Date:100","Tipe:Data:100","Jumlah Penerimaan:Float:100","UOM:Data:100","Jumlah Pc Diterima:Float:100"]
	
	date_clause = ""
	if filters.get("from_date") and filters.get("to_date") :
		date_clause = """ AND i.`posting_date` BETWEEN "{0}" AND "{1}" """.format(filters.get("from_date"),filters.get("to_date"))
	
	item_clause = ""
	if filters.get("item") :
		item_clause = """ AND j.`item_code`="{0}" """.format(filters.get("item"))
	
	recon_clause = ""
	if filters.get("stock_recon") :
		supplier_clause = """ AND i.`name` = "{0}" """.format(filters.get("stock_recon"))
		
	data = frappe.db.sql(""" SELECT j.`item_code`,i.`posting_date`,j.`total_roll_from`,j.`total_roll_to`,
		j.`yard_atau_meter_per_roll_from`,j.`yard_atau_meter_per_roll_to`,k.`stock_uom` 
		FROM `tabStock Recon Inventory`i JOIN `tabStock Recon Inventory Item`j ON i.`name`=j.`parent` 
		JOIN `tabItem`k ON k.`name`=j.`item_code` WHERE i.`docstatus`=1 
		{0} {1} {2}
		GROUP BY j.`item_code`
		""".format(date_clause,item_clause,recon_clause),as_list =1)
	
	data_mod = []
	for res in data :
		res_mod = [res[0],res[1]]
		roll_change = res[3] - res[2]
		total_change = res[3] * res[5] - res[4] * res[2]
		type = ""
		if total_change < 0 :
			type = "Out"
		else :
			type = "In"
		uom = res[6]
		res_mod = res_mod + [type,total_change,uom,roll_change]
		data_mod.append(res_mod)
		
	data =  frappe.db.sql(""" SELECT j.`item_code_pcs`,i.`posting_date`,j.`total_pcs_from`,j.`total_pcs_to`,j.`uom_pcs` 
		FROM `tabStock Recon Inventory`i JOIN `tabStock Recon Inventory Pcs`j ON i.`name`=j.`parent`  
		WHERE i.`docstatus`=1 {0} {1} {2} GROUP BY j.`item_code_pcs` """.format(item_clause,date_clause,recon_clause),as_list=1)
	
	for res in data :
		res_mod = [res[0],res[1]]
		change = res[3] - res[2]
		uom = res[5]
		type = ""
		if total_change < 0 :
			type = "Out"
		else :
			type = "In"
		res_mod = res_mod + [type,change,uom,change]
		data_mod.append(res_mod)
	return columns, data_mod
