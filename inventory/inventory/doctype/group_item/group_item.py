# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


from frappe import msgprint
import frappe.utils
from frappe.utils import cstr, flt, getdate, comma_and, cint
from frappe import _
from frappe.model.mapper import get_mapped_doc
import operator

class GroupItem(Document):
	pass
	

@frappe.whitelist()
def save_group_item(doc,method):
	temp = ""
	if doc.data_group :
		for i in doc.data_group :
			cek_data = frappe.db.sql("""
					SELECT 
					di.`item_code_variant`,
					di.`total_roll`,
					di.`total_yard_atau_meter`
					FROM `tabData Inventory` di
					WHERE di.`item_code_variant` = "{}"
					and di.`yard_atau_meter_per_roll` = "{}"
					and di.`warehouse` = "{}"
					and di.`colour` = "{}"
					and di.`inventory_uom` = "{}"
				""".format(i.item_code_variant, i.yard_atau_meter, i.warehouse, i.colour,  i.inventory_uom))

			if cek_data :
				count = 0
			else :
				temp = temp + "(" + str(i.item_code_variant) + "," + str(i.yard_atau_meter) + "," + str(i.colour) + ") "

		if temp :
			frappe.throw("Item "+temp+" tidak ada di dalam inventory")


@frappe.whitelist()
def submit_group_item(doc,method):
	count = 0

	# belum pengecekan apakah itemnya ada di master inventory apa ndak

	if doc.packing_list_receipt :
		count = 1

	else :
		for i in doc.data_group :
			mi = frappe.get_doc("Master Inventory", i.item_code_variant)
			mi.append("data_inventory", {
				"doctype": "Data Inventory",
				"item_code_variant" : i.item_code_variant,
				"yard_atau_meter_per_roll" : i.yard_atau_meter,
				"total_roll" : i.total_qty_roll,
				"total_yard_atau_meter" : i.yard_atau_meter * i.total_qty_roll,
				"warehouse" : i.warehouse,
				"colour" : i.colour,
				"group" : doc.group_code,
				"inventory_uom" : i.inventory_uom
			})

			cek_data = frappe.db.sql("""
				SELECT 
				di.`item_code_variant`,
				di.`total_roll`,
				di.`total_yard_atau_meter`
				FROM `tabData Inventory` di
				WHERE di.`item_code_variant` = "{}"
				and di.`yard_atau_meter_per_roll` = "{}"
				and di.`warehouse` = "{}"
				and di.`colour` = "{}"
				and di.`inventory_uom` = "{}"
			""".format(i.item_code_variant, i.yard_atau_meter, i.warehouse, i.colour,  i.inventory_uom))
			
			if cek_data :
				current_total_roll = cek_data[0][1]
				current_total_yard = cek_data[0][2]

				new_total_roll = current_total_roll - i.total_qty_roll
				new_total_yard = current_total_yard - (i.yard_atau_meter * i.total_qty_roll)

				frappe.db.sql ("""
					UPDATE 
					`tabData Inventory` di
					SET 
					di.`total_roll`="{0}",
					di.`total_yard_atau_meter`="{1}"
					WHERE di.`item_code_variant`="{2}"
					AND di.`yard_atau_meter_per_roll`="{3}"
					AND di.`warehouse`="{4}"
					AND di.`colour` = "{5}"
					AND di.`inventory_uom` = "{6}"

					""".format(new_total_roll, new_total_yard, i.item_code_variant, i.yard_atau_meter, i.warehouse, i.colour, i.inventory_uom))

		mi.flags.ignore_permissions = 1
		mi.submit()


@frappe.whitelist()
def cancel_group_item(doc,method):
	if doc.packing_list_receipt :
		# menghapus data group dari packing list receipt nya 
		frappe.throw("Tidak dapat menghapus karena terhubung dengan Packing List Receipt")
	else :
		if doc.is_used == 1 :
			frappe.throw("Tidak dapat di cancel karen Group telah di gunakan")
		else :
			cek_data = frappe.db.sql("""
				SELECT 
				di.`item_code_variant`,
				di.`total_roll`,
				di.`total_yard_atau_meter`
				FROM `tabData Inventory` di
				WHERE di.`item_code_variant` = "{}"
				and di.`yard_atau_meter_per_roll` = "{}"
				and di.`warehouse` = "{}"
				and di.`colour` = "{}"
				and di.`inventory_uom` = "{}"
			""".format(i.item_code_variant, i.yard_atau_meter, i.warehouse, i.colour,  i.inventory_uom))
			
			if cek_data :
				current_total_roll = cek_data[0][1]
				current_total_yard = cek_data[0][2]

				new_total_roll = current_total_roll + i.total_roll
				new_total_yard = current_total_yard + (i.yard_atau_meter * i.total_roll)

				frappe.db.sql ("""
					UPDATE 
					`tabData Inventory` di
					SET 
					di.`total_roll`="{0}",
					di.`total_yard_atau_meter`="{1}"
					WHERE di.`item_code_variant`="{2}"
					AND di.`yard_atau_meter_per_roll`="{3}"
					AND di.`warehouse`="{4}"
					AND di.`colour` = "{5}"
					AND di.`inventory_uom` = "{6}"

					""".format(new_total_roll, new_total_yard, i.item_code_variant, i.yard_atau_meter, i.warehouse, i.colour, i.inventory_uom))

			frappe.db.sql ("""
				DELETE FROM 
				`tabData Inventory` di
				WHERE di.`item_code_variant`="{0}"
				AND di.`yard_atau_meter_per_roll`="{1}"
				AND di.`warehouse`="{2}"
				AND di.`colour` = "{3}"
				AND di.`inventory_uom` = "{4}"
				AND di.`group` = "{5}"

				""".format(i.item_code_variant, i.yard_atau_meter, i.warehouse, i.colour, i.inventory_uom, doc.group_code))