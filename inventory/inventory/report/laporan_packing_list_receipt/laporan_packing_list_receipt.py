# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	
	columns = ["Produk:Link/Item:100","Tanggal PO:Date:100","Nomor PO:Link/Purchase Order:100","Supplier:Link/Supplier:100","Supplier Group:Data:100",
		"Territory:Data:100","Qty Ordered:Float:100","Jumlah Pc Dipesan:Float:100","UOM:Data:100","Tanggal PLR:Date:100","Nomor PLR:Link/Packing List Receipt:100",
		"Jumlah Penerimaan:Float:100","Jumlah Pc Diterima:Float:100","Keterangan:Data:200"]
	
	date_clause = ""
	if filters.get("from_date") and filters.get("to_date") :
		date_clause = """ AND po.`transaction_date` BETWEEN "{0}" AND "{1}" """.format(filters.get("from_date"),filters.get("to_date"))
	
	item_clause = ""
	if filters.get("item") :
		item_clause = """ AND po.`name`="{0}" """.format(filters.get("item"))
	
	supplier_clause = ""
	if filters.get("supplier") :
		supplier_clause = """ AND po.`supplier` = "{0}" """.format(filters.get("supplier"))
		
	data = frappe.db.sql(""" SELECT poi.`item_code`,po.`transaction_date`,po.`name`,po.`supplier`,s.`supplier_type`,s.`territory`,
		poi.`qty`,poi.`roll_qty`,poi.`uom`, plr.`posting_date`,plr.`name`
		FROM `tabPurchase Order`po JOIN `tabPurchase Order Item`poi ON po.`name`=poi.`parent`
		JOIN `tabSupplier`s ON po.`supplier`= s.`name`
		JOIN `tabPacking List Receipt`plr ON plr.`purchase_order`=po.`name` AND plr.`docstatus`=1
		{0} {1} {2}
		GROUP BY poi.`item_code`
		""".format(date_clause,item_clause,supplier_clause),as_list=1)
	
	plr_list = []
	plr_clause = ""
	for res in data :
		if res[10] :
			if res[10] not in plr_list :
				plr_list.append(res[10])
				if plr_clause == "" :
					plr_clause = """ ("{0}" """.format(res[10])
				else :
					plr_clause = """ {0}, "{1}" """.format(plr_clause,res[10])
	if plr_clause == "" :
		return columns,[]
	plr_clause = plr_clause + ")"
	data_col = frappe.db.sql(""" SELECT i.`parent`,i.`item_code_variant`,i.`total_yard_atau_meter`,i.`total_roll`,i.`keterangan_group` 
		FROM `tabPacking List Receipt Data`i WHERE i.`parent` IN {0} """.format(plr_clause),as_list=1) 
	data_col_2 = frappe.db.sql(""" SELECT i.`parent`,i.`item_code_pcs`,0,i.`total_pcs`,"" FROM `tabPacking List Receipt PCS`i 
		WHERE i.`parent` IN {0}	""".format(plr_clause),as_list=1)
	data_col = data_col + data_col_2
	
	new_data = {}
	new_data_roll = {}
	new_data_ket = {}
	for item in data_col :
		key = (item[0],item[1])
		if not key in new_data :
			new_data[key] = 0.0
			new_data_roll[key] = 0.0
			new_data_ket[key] = item[4] or ""
		new_data[key] = new_data[key] + item[2]
		new_data_roll[key] = new_data_roll[key] + item[3]
	
	data_2 = []
	for res in data :
		key = (res[10],res[0])
		
		if key in new_data :
			res = res + [new_data[key],new_data_roll[key],new_data_ket[key]]
			data_2.append(res)
		else :
			res = res + [0,0,""]
	return columns, data_2
