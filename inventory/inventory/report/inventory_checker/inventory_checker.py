# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	
	columns = ["Item Code:Link/Item:200","Colour:Data:100","Yard/Meter per Roll:Float:100","UOM:Data:100","Group:Data:100","Total:Float:100","Status:Data:100",
		"Val. Item Code:Link/Item:200","Val. Colour:Data:100","Val. Yard/Meter per Roll:Float:100","Val. UOM:Data:100","Val. Group:Data:100","Val. Total:Float:100"]
		
	frappe.msgprint(filters.get("inventory_validator"))
	doc = frappe.get_doc("Inventory Validator", filters.get("inventory_validator"))
	
	
	data = []
	for item in doc.get("data_inventory_unchecked"):
		data.append([item.item_code_variant,item.colour,item.yard_atau_meter_per_roll,item.inventory_uom,item.group,item.total_roll,"Unchecked",
			"","","","","",""])
	for item in doc.get("data_inventory_missing"):
		data.append(["","","","","","","Missing",
			item.item_code_variant,item.colour,item.yard_atau_meter_per_roll,item.inventory_uom,item.group,item.total_roll])
	for item in doc.get("data_inventory_checked"):
		data.append([item.item_code_variant,item.colour,item.yard_atau_meter_per_roll,item.inventory_uom,item.group,item.total_roll,"Unchecked",
			item.item_code_variant,item.colour,item.yard_atau_meter_per_roll,item.inventory_uom,item.group,item.total_roll])
	
	
	return columns, data
