# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	
	columns = ["Item Code:Link/Item:200","Colour:Data:100","Yard/Meter per Roll:Float:100","UOM:Data:100","Group:Data:100","Total:Float:100","Status:Data:100",
		"Val. Item Code:Link/Item:200","Val. Colour:Data:100","Val. Yard/Meter per Roll:Float:100","Val. UOM:Data:100","Val. Group:Data:100","Val. Total:Float:100"]
		
	receipt_no = filters.get("packing_list_receipt")
	validate_no = frappe.db.sql("""SELECT i.`name` FROM `tabPacking List Receipt Validator`i WHERE i.`from_packing_list_receipt`="{0}" """.format(receipt_no))
	if len(validate_no)<1 :
		return [], []
	validate_no = validate_no[0]
	validate_no = validate_no[0]
	
	slrv = frappe.get_doc("Packing List Receipt Validator",validate_no)
	slr = frappe.get_doc("Packing List Receipt",receipt_no)
	
	data_title = []
	data_item = {}
	for item in slr.packing_list_data :
		data_title.append(item.name)
		data_item[item.name] = item
	pcs_title = []
	pcs_item = {}
	for item in slr.packing_list_data_pcs :
		pcs_title.append(item.name)
		pcs_item[item.name] = item
	
	data = []
	
	
	
	for item in slrv.packing_list_data_unchecked :
		data.append(["","","","","","","Unchecked",
			item.item_code_variant,item.colour,item.yard_atau_meter_per_roll,item.inventory_uom,item.group,item.total_roll])
	for item in slrv.packing_list_pcs_unchecked :
		data.append(["","","","","","","Unchecked",
			item.item_code_pcs,"","",item.uom_pcs,"",item.total_pcs,])
	for item in slrv.packing_list_data_missing :
		data.append(["","","","","","","Missing",
			item.item_code_variant,item.colour,item.yard_atau_meter_per_roll,item.inventory_uom,item.group,item.total_roll])
	for item in slrv.packing_list_pcs_missing :
		data.append(["","","","","","","Missing",
			item.item_code_pcs,"","",item.uom_pcs,"",item.total_pcs])
	for item in slrv.packing_list_data_checked :
		
		s_item = data_item[item.from_data]
		data.append([s_item.item_code_variant,s_item.colour,s_item.yard_atau_meter_per_roll,s_item.inventory_uom,s_item.group,s_item.total_roll,"Checked",
			item.item_code_variant,item.colour,item.yard_atau_meter_per_roll,item.inventory_uom,item.group,item.total_roll])
	for item in slrv.packing_list_pcs_checked :
		s_item = pcs_item[item.from_data]
		data.append([s_item.item_code_pcs,"","",s_item.uom_pcs,"",s_item.total_pcs,"Checked",
			item.item_code_pcs,"","",item.uom_pcs,"",item.total_pcs])
	
			
	return columns, data
