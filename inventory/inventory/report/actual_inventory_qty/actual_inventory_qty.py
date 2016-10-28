# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	
	columns = ["Colour:Link/Colour:100","Group:Data:100","Yard/Meter per Roll:Float:100","UOM:Link/UOM:100","Total Roll:Float:100","Total Yard/Meter:Float:100"]
	
	item_clause = ""
	if filters.get("item"):
		item_clause = """ AND mi.`item_code`="{0}" """.format(filters.get("item"))
	
	colour_clause = ""
	if filters.get("colour"):
		colour_clause = """ AND di.`colour`="{0}" """.format(filters.get("colour"))
	
	group_clause = ""
	if filters.get("group"):
		group_clause = """ AND di.`group`="{0}" """.format(filters.get("group"))
	
	negative_clause = ""
	if filters.get("is_negative"):
		negative_clause = """ AND di.`total_roll`<0 """
	
	result = frappe.db.sql("""
		SELECT mi.`item_code`,di.`colour`,di.`group`,di.`yard_atau_meter_per_roll`,di.`inventory_uom`,di.`total_roll`,di.`total_yard_atau_meter` 
		FROM `tabMaster Inventory`mi JOIN `tabData Inventory`di ON di.`parent` = mi.`name` WHERE di.`total_roll`!=0
		{0} {1} {2} {3}
		ORDER BY mi.`item_code`
		""".format(item_clause,colour_clause,group_clause,negative_clause),as_list=1)
	
	data = []
	cur_item = ""
	for res in result :
		if not res[0] == cur_item :
			cur_item = res[0]
			data.append([res[0],"","","","",""])
		res.pop(0)
		data.append(res)
	
	return columns, data
