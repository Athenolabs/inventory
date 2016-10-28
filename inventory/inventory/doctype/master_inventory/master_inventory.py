# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class MasterInventory(Document):
	pass

# @frappe.whitelist()
# def submit_purchase_receipt(doc,method):
# 	for i in doc.items :
# 		if i.parent_item :
# 			cek_inventory = frappe.db.sql("""
# 				SELECT
# 				mi.`item_code`
# 				FROM `tabMaster Inventory` mi
# 				WHERE mi.`item_code` = "{}"
# 				""".format(i.parent_item))

# 			if cek_inventory :
# 				cek_data = frappe.db.sql("""
# 					SELECT 
# 					di.`item_code_variant`,
# 					di.`total_roll`,
# 					di.`total_yard`
# 					FROM `tabData Inventory` di
# 					WHERE di.`parent` = "{}"
# 					AND di.`item_code_variant` = "{}"
# 					and di.`yard_per_roll` = "{}"
# 				""".format(i.parent_item, i.item_code, i.yard_per_roll))

# 				if cek_data :
# 					current_total_roll = cek_data[0][1]
# 					current_total_yard = cek_data[0][2]

# 					new_total_roll = current_total_roll + (i.qty / i.yard_per_roll)
# 					new_total_yard = current_total_yard + i.qty

# 					frappe.db.sql ("""
# 						update 
# 						`tabData Inventory` 
# 						set 
# 						total_roll="{0}",
# 						total_yard="{1}"
# 						where 
# 						parent="{2}"
# 						AND
# 						item_code_variant="{3}"
# 						AND
# 						yard_per_roll="{4}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll))

# 					# frappe.db.commit()

# 				else :
# 					temp_colour = frappe.db.sql("""
# 					SELECT iva.`parent`, iva.`attribute_value` FROM `tabItem Variant Attribute` iva
# 					WHERE iva.`parent` = "{}"
# 					""".format(i.item_code))

# 					colour = temp_colour[0][1]
# 					mi = frappe.get_doc("Master Inventory", i.parent_item)
# 					mi.append("data_inventory", {
# 						"doctype": "Data Inventory",
# 						"item_code_variant" : i.item_code,
# 						"colour" : colour,
# 						"warehouse" : i.warehouse,
# 						"yard_per_roll" : i.yard_per_roll,
# 						"total_roll" : (i.qty/i.yard_per_roll),
# 						"total_yard" : i.qty
# 					})

# 					mi.flags.ignore_permissions = 1
# 					mi.save()

# 			else :
# 				item = frappe.get_doc("Item", i.parent_item)
# 				mi = frappe.new_doc("Master Inventory")
# 				mi.update({
# 					"item_code": item.item_code,
# 					"item_name": item.item_name,
# 					"design": item.design		
# 				})

# 				temp_colour = frappe.db.sql("""
# 					SELECT iva.`parent`, iva.`attribute_value` FROM `tabItem Variant Attribute` iva
# 					WHERE iva.`parent` = "{}"
# 					""".format(i.item_code))

# 				colour = temp_colour[0][1]
# 				mi.append("data_inventory", {
# 					"doctype": "Data Inventory",
# 					"item_code_variant" : i.item_code,
# 					"colour" : colour,
# 					"warehouse" : i.warehouse,
# 					"yard_per_roll" : i.yard_per_roll,
# 					"total_roll" : (i.qty/i.yard_per_roll),
# 					"total_yard" : i.qty
# 				})

# 				mi.flags.ignore_permissions = 1
# 				mi.save()

# @frappe.whitelist()
# def cancel_purchase_receipt(doc,method):
# 	for i in doc.items :
# 		if i.parent_item :
# 			cek_inventory = frappe.db.sql("""
# 				SELECT
# 				mi.`item_code`
# 				FROM `tabMaster Inventory` mi
# 				WHERE mi.`item_code` = "{}"
# 				""".format(i.parent_item))

# 			if cek_inventory :
# 				cek_data = frappe.db.sql("""
# 					SELECT 
# 					di.`item_code_variant`,
# 					di.`total_roll`,
# 					di.`total_yard`
# 					FROM `tabData Inventory` di
# 					WHERE di.`parent` = "{}"
# 					AND di.`item_code_variant` = "{}"
# 					and di.`yard_per_roll` = "{}"
# 				""".format(i.parent_item, i.item_code, i.yard_per_roll))

# 				if cek_data :
# 					current_total_roll = cek_data[0][1]
# 					current_total_yard = cek_data[0][2]

# 					new_total_roll = current_total_roll - (i.qty / i.yard_per_roll)
# 					new_total_yard = current_total_yard - i.qty

# 					frappe.db.sql ("""
# 						update 
# 						`tabData Inventory` 
# 						set 
# 						total_roll="{0}",
# 						total_yard="{1}"
# 						where 
# 						parent="{2}"
# 						AND
# 						item_code_variant="{3}"
# 						AND
# 						yard_per_roll="{4}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll))

# 					# frappe.db.commit()


# @frappe.whitelist()
# def submit_delivery_note(doc,method):
# 	for i in doc.items :
# 		if i.parent_item :
# 			cek_inventory = frappe.db.sql("""
# 				SELECT
# 				mi.`item_code`
# 				FROM `tabMaster Inventory` mi
# 				WHERE mi.`item_code` = "{}"
# 				""".format(i.parent_item))

# 			if cek_inventory :
# 				cek_data = frappe.db.sql("""
# 					SELECT 
# 					di.`item_code_variant`,
# 					di.`total_roll`,
# 					di.`total_yard`
# 					FROM `tabData Inventory` di
# 					WHERE di.`parent` = "{}"
# 					AND di.`item_code_variant` = "{}"
# 					and di.`yard_per_roll` = "{}"
# 				""".format(i.parent_item, i.item_code, i.yard_per_roll))

# 				if cek_data :
# 					current_total_roll = cek_data[0][1]
# 					current_total_yard = cek_data[0][2]

# 					new_total_roll = current_total_roll - (i.qty / i.yard_per_roll)
# 					new_total_yard = current_total_yard - i.qty

# 					frappe.db.sql ("""
# 						update 
# 						`tabData Inventory` 
# 						set 
# 						total_roll="{0}",
# 						total_yard="{1}"
# 						where 
# 						parent="{2}"
# 						AND
# 						item_code_variant="{3}"
# 						AND
# 						yard_per_roll="{4}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll))

# 					# frappe.db.commit()


# @frappe.whitelist()
# def cancel_delivery_note(doc,method):
# 	for i in doc.items :
# 		if i.parent_item :
# 			cek_inventory = frappe.db.sql("""
# 				SELECT
# 				mi.`item_code`
# 				FROM `tabMaster Inventory` mi
# 				WHERE mi.`item_code` = "{}"
# 				""".format(i.parent_item))

# 			if cek_inventory :
# 				cek_data = frappe.db.sql("""
# 					SELECT 
# 					di.`item_code_variant`,
# 					di.`total_roll`,
# 					di.`total_yard`
# 					FROM `tabData Inventory` di
# 					WHERE di.`parent` = "{}"
# 					AND di.`item_code_variant` = "{}"
# 					and di.`yard_per_roll` = "{}"
# 				""".format(i.parent_item, i.item_code, i.yard_per_roll))

# 				if cek_data :
# 					current_total_roll = cek_data[0][1]
# 					current_total_yard = cek_data[0][2]

# 					new_total_roll = current_total_roll + (i.qty / i.yard_per_roll)
# 					new_total_yard = current_total_yard + i.qty

# 					frappe.db.sql ("""
# 						update 
# 						`tabData Inventory` 
# 						set 
# 						total_roll="{0}",
# 						total_yard="{1}"
# 						where 
# 						parent="{2}"
# 						AND
# 						item_code_variant="{3}"
# 						AND
# 						yard_per_roll="{4}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll))

# 					# frappe.db.commit()




@frappe.whitelist()
def submit_packing_list_receipt(doc,method):
	for i in doc.packing_list_data :
		if i.item_code_variant :
			cek_inventory = frappe.db.sql("""
				SELECT
				mi.`item_code`
				FROM `tabMaster Inventory` mi
				WHERE mi.`item_code` = "{}"
				""".format(i.item_code_variant))

			if cek_inventory :
				if i.group :
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
						and di.`group` = "{}"
						and di.`inventory_uom` = "{}"
					""".format(i.item_code_variant, i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))

					if cek_data :
						current_total_roll = cek_data[0][1]
						current_total_yard = cek_data[0][2]

						new_total_roll = current_total_roll + i.total_roll
						new_total_yard = current_total_yard + i.total_yard_atau_meter

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
							AND di.`group` = "{6}"
							AND di.`inventory_uom` = "{7}"

							 """.format(new_total_roll,new_total_yard,i.item_code_variant,i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))

						# frappe.db.commit()

					else :
						
						mi = frappe.get_doc("Master Inventory", i.item_code_variant)
						mi.append("data_inventory", {
							"doctype": "Data Inventory",
							"item_code_variant" : i.item_code_variant,
							"yard_atau_meter_per_roll" : i.yard_atau_meter_per_roll,
							"total_roll" : i.total_roll,
							"total_yard_atau_meter" : i.total_yard_atau_meter,
							"warehouse" : i.warehouse,
							"colour" : i.colour,
							"group" : i.group,
							"inventory_uom" : i.inventory_uom
						})

						mi.flags.ignore_permissions = 1
						mi.save()
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
						and di.`group` is null
					""".format(i.item_code_variant, i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.inventory_uom))

					if cek_data :
						current_total_roll = cek_data[0][1]
						current_total_yard = cek_data[0][2]

						new_total_roll = current_total_roll + i.total_roll
						new_total_yard = current_total_yard + i.total_yard_atau_meter

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
							and di.`group` is null

							 """.format(new_total_roll,new_total_yard,i.item_code_variant,i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.inventory_uom))

						# frappe.db.commit()

					else :
						
						mi = frappe.get_doc("Master Inventory", i.item_code_variant)
						mi.append("data_inventory", {
							"doctype": "Data Inventory",
							"item_code_variant" : i.item_code_variant,
							"yard_atau_meter_per_roll" : i.yard_atau_meter_per_roll,
							"total_roll" : i.total_roll,
							"total_yard_atau_meter" : i.total_yard_atau_meter,
							"warehouse" : i.warehouse,
							"colour" : i.colour,
							"inventory_uom" : i.inventory_uom
						})

						mi.flags.ignore_permissions = 1
						mi.save()

			else :
				item = frappe.get_doc("Item", i.item_code_variant)
				mi = frappe.new_doc("Master Inventory")
				mi.update({
					"item_code": item.item_code,
					"item_name": item.item_name	
				})

				if i.group :
					mi.append("data_inventory", {
						"doctype": "Data Inventory",
						"item_code_variant" : i.item_code_variant,
						"yard_atau_meter_per_roll" : i.yard_atau_meter_per_roll,
						"total_roll" : i.total_roll,
						"total_yard_atau_meter" : i.total_yard_atau_meter,
						"warehouse" : i.warehouse,
						"colour" : i.colour,
						"group" : i.group,
						"inventory_uom" : i.inventory_uom
					})
				else :
					mi.append("data_inventory", {
						"doctype": "Data Inventory",
						"item_code_variant" : i.item_code_variant,
						"yard_atau_meter_per_roll" : i.yard_atau_meter_per_roll,
						"total_roll" : i.total_roll,
						"total_yard_atau_meter" : i.total_yard_atau_meter,
						"warehouse" : i.warehouse,
						"colour" : i.colour,
						"inventory_uom" : i.inventory_uom
					})

				mi.flags.ignore_permissions = 1
				mi.save()


@frappe.whitelist()
def cancel_packing_list_receipt(doc,method):
	for i in doc.packing_list_data :
		if i.item_code_variant :
			cek_inventory = frappe.db.sql("""
				SELECT
				mi.`item_code`
				FROM `tabMaster Inventory` mi
				WHERE mi.`item_code` = "{}"
				""".format(i.item_code_variant))

			if cek_inventory :
				if i.group :
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
						and di.`group` = "{}"
						and di.`inventory_uom` = "{}"
					""".format(i.item_code_variant, i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))
					
					if cek_data :
						current_total_roll = cek_data[0][1]
						current_total_yard = cek_data[0][2]

						new_total_roll = current_total_roll - i.total_roll
						new_total_yard = current_total_yard - i.total_yard_atau_meter

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
							AND di.`group` = "{6}"
							AND di.`inventory_uom` = "{7}"

							""".format(new_total_roll,new_total_yard,i.item_code_variant,i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))

						# frappe.db.commit()
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
						and di.`group` is null
					""".format(i.item_code_variant, i.yard_atau_meter_per_roll, i.warehouse, i.colour,  i.inventory_uom))
					
					if cek_data :
						if cek_data[0][1] < i.total_roll :
							frappe.throw("Tidak bisa di cancel karena item sudah di gunakan (qty di inventory lebih kecil dari qty packing list receipt)")
						else :
							current_total_roll = cek_data[0][1]
							current_total_yard = cek_data[0][2]

							new_total_roll = current_total_roll - i.total_roll
							new_total_yard = current_total_yard - i.total_yard_atau_meter

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
								and di.`group` is null

								""".format(new_total_roll,new_total_yard,i.item_code_variant,i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.inventory_uom))

						# frappe.db.commit()



@frappe.whitelist()
def submit_packing_list_delivery(doc,method):
	# get_pending_order = frappe.db.sql("""
	# 	SELECT 
	# 	dni.`pending_order`
	# 	FROM `tabDelivery Note Item` dni
	# 	WHERE dni.`parent` = "{}"
	# 	GROUP BY dni.`pending_order`
	# 	""".format(doc.name))

	# for z in get_pending_order :

	# 	get_data = frappe.db.sql("""
	# 		SELECT
	# 		pld.`name`,
	# 		pldd.`item_code_variant`,
	# 		pldd.`yard_atau_meter_per_roll`,
	# 		pldd.`warehouse`,
	# 		pldd.`colour`,
	# 		pldd.`group`,
	# 		pldd.`inventory_uom`,
	# 		pldd.`total_roll`,
	# 		pldd.`total_yard_atau_meter`
	# 		FROM
	# 		`tabPacking List Delivery` pld
	# 		JOIN `tabPacking List Delivery Data` pldd
	# 		ON pld.`name` = pldd.`parent`
	# 		WHERE pld.`name` = "{}"
	# 	""".format(z[0]))


	for i in doc.packing_list_data :
		if i.group :
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
				and di.`group` = "{}"
				and di.`inventory_uom` = "{}"
			""".format(i.item_code_roll, i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))

			

			if cek_data :
				current_total_roll = cek_data[0][1]
				current_total_yard = cek_data[0][2]

				new_total_roll = current_total_roll - i.roll_qty
				new_total_yard = current_total_yard - i.total_yard_atau_meter



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
					AND di.`group` = "{6}"
					AND di.`inventory_uom` = "{7}"

					 """.format(new_total_roll, new_total_yard, i.item_code_roll, i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))

				# frappe.db.commit()

			
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
				and di.`group` is null
				and di.`inventory_uom` = "{}"
			""".format(i.item_code_roll, i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.inventory_uom))

			if cek_data :
				current_total_roll = cek_data[0][1]
				current_total_yard = cek_data[0][2]

				new_total_roll = current_total_roll - i.roll_qty
				new_total_yard = current_total_yard - i.total_yard_atau_meter

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
					and di.`group` is null

					 """.format(new_total_roll, new_total_yard, i.item_code_roll, i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.inventory_uom))

				# frappe.db.commit()



@frappe.whitelist()
def cancel_packing_list_delivery(doc,method):
	# get_pending_order = frappe.db.sql("""
	# 	SELECT 
	# 	dni.`pending_order`
	# 	FROM `tabDelivery Note Item` dni
	# 	WHERE dni.`parent` = "{}"
	# 	GROUP BY dni.`pending_order`
	# 	""".format(doc.name))

	# for z in get_pending_order :

	# 	get_data = frappe.db.sql("""
	# 		SELECT
	# 		pld.`name`,
	# 		pldd.`item_code_variant`,
	# 		pldd.`yard_atau_meter_per_roll`,
	# 		pldd.`warehouse`,
	# 		pldd.`colour`,
	# 		pldd.`group`,
	# 		pldd.`inventory_uom`,
	# 		pldd.`total_roll`,
	# 		pldd.`total_yard_atau_meter`
	# 		FROM
	# 		`tabPacking List Delivery` pld
	# 		JOIN `tabPacking List Delivery Data` pldd
	# 		ON pld.`name` = pldd.`parent`
	# 		WHERE pld.`name` = "{}"
	# 	""".format(z[0]))

	for i in doc.packing_list_data :
		if i.group :
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
				and di.`group` = "{}"
				and di.`inventory_uom` = "{}"
			""".format(i.item_code_roll, i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))

			if cek_data :
				current_total_roll = cek_data[0][1]
				current_total_yard = cek_data[0][2]

				new_total_roll = current_total_roll + i.roll_qty
				new_total_yard = current_total_yard + i.total_yard_atau_meter

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
					AND di.`group` = "{6}"
					AND di.`inventory_uom` = "{7}"

					 """.format(new_total_roll, new_total_yard, i.item_code_roll, i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))

				# frappe.db.commit()

			
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
				and di.`group` is null
				and di.`inventory_uom` = "{}"
			""".format(i.item_code_roll, i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.inventory_uom))

			if cek_data :
				current_total_roll = cek_data[0][1]
				current_total_yard = cek_data[0][2]

				new_total_roll = current_total_roll + i.roll_qty
				new_total_yard = current_total_yard + i.total_yard_atau_meter

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
					and di.`group` is null
					 """.format(new_total_roll, new_total_yard, i.item_code_roll, i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.inventory_uom))

				# frappe.db.commit()




# @frappe.whitelist()
# def submit_stock_entry(doc,method):
# 	if doc.purpose == "Material Receipt" :
# 		for i in doc.items :
# 			if i.parent_item :
# 				cek_inventory = frappe.db.sql("""
# 					SELECT
# 					mi.`item_code`
# 					FROM `tabMaster Inventory` mi
# 					WHERE mi.`item_code` = "{}"
# 					""".format(i.parent_item))

# 				if cek_inventory :
# 					cek_data = frappe.db.sql("""
# 						SELECT 
# 						di.`item_code_variant`,
# 						di.`total_roll`,
# 						di.`total_yard`
# 						FROM `tabData Inventory` di
# 						WHERE di.`parent` = "{}"
# 						AND di.`item_code_variant` = "{}"
# 						and di.`yard_per_roll` = "{}"
# 						and di.`warehouse` = "{}"
# 					""".format(i.parent_item, i.item_code, i.yard_per_roll, i.t_warehouse))

# 					if cek_data :
# 						current_total_roll = cek_data[0][1]
# 						current_total_yard = cek_data[0][2]

# 						new_total_roll = current_total_roll + (i.qty / i.yard_per_roll)
# 						new_total_yard = current_total_yard + i.qty

# 						frappe.db.sql ("""
# 							update 
# 							`tabData Inventory` 
# 							set 
# 							total_roll="{0}",
# 							total_yard="{1}"
# 							where 
# 							parent="{2}"
# 							AND
# 							item_code_variant="{3}"
# 							AND
# 							yard_per_roll="{4}"
# 							and
# 							warehouse="{5}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll, i.t_warehouse))

# 						# frappe.db.commit()

# 					else :
# 						temp_colour = frappe.db.sql("""
# 						SELECT iva.`parent`, iva.`attribute_value` FROM `tabItem Variant Attribute` iva
# 						WHERE iva.`parent` = "{}"
# 						""".format(i.item_code))

# 						colour = temp_colour[0][1]
# 						mi = frappe.get_doc("Master Inventory", i.parent_item)
# 						mi.append("data_inventory", {
# 							"doctype": "Data Inventory",
# 							"item_code_variant" : i.item_code,
# 							"colour" : colour,
# 							"warehouse" : i.t_warehouse,
# 							"yard_per_roll" : i.yard_per_roll,
# 							"total_roll" : (i.qty/i.yard_per_roll),
# 							"total_yard" : i.qty,

# 						})

# 						mi.flags.ignore_permissions = 1
# 						mi.save()

# 				else :
# 					item = frappe.get_doc("Item", i.parent_item)
# 					mi = frappe.new_doc("Master Inventory")
# 					mi.update({
# 						"item_code": item.item_code,
# 						"item_name": item.item_name,
# 						"design": item.design		
# 					})

# 					temp_colour = frappe.db.sql("""
# 					SELECT iva.`parent`, iva.`attribute_value` FROM `tabItem Variant Attribute` iva
# 					WHERE iva.`parent` = "{}"
# 					""".format(i.item_code))

# 					colour = temp_colour[0][1]
# 					mi.append("data_inventory", {
# 						"doctype": "Data Inventory",
# 						"item_code_variant" : i.item_code,
# 						"colour" : colour,
# 						"warehouse" : i.t_warehouse,
# 						"yard_per_roll" : i.yard_per_roll,
# 						"total_roll" : (i.qty/i.yard_per_roll),
# 						"total_yard" : i.qty
# 					})

# 					mi.flags.ignore_permissions = 1
# 					mi.save()


# 	elif doc.purpose == "Material Issue" :
# 		for i in doc.items :
# 			if i.parent_item :
# 				cek_inventory = frappe.db.sql("""
# 					SELECT
# 					mi.`item_code`
# 					FROM `tabMaster Inventory` mi
# 					WHERE mi.`item_code` = "{}"
# 					""".format(i.parent_item))

# 				if cek_inventory :
# 					cek_data = frappe.db.sql("""
# 						SELECT 
# 						di.`item_code_variant`,
# 						di.`total_roll`,
# 						di.`total_yard`
# 						FROM `tabData Inventory` di
# 						WHERE di.`parent` = "{}"
# 						AND di.`item_code_variant` = "{}"
# 						and di.`yard_per_roll` = "{}"
# 						and di.`warehouse` = "{}"
# 					""".format(i.parent_item, i.item_code, i.yard_per_roll, i.s_warehouse))

# 					if cek_data :
# 						current_total_roll = cek_data[0][1]
# 						current_total_yard = cek_data[0][2]

# 						new_total_roll = current_total_roll - (i.qty / i.yard_per_roll)
# 						new_total_yard = current_total_yard - i.qty

# 						frappe.db.sql ("""
# 							update 
# 							`tabData Inventory` 
# 							set 
# 							total_roll="{0}",
# 							total_yard="{1}"
# 							where 
# 							parent="{2}"
# 							AND
# 							item_code_variant="{3}"
# 							AND
# 							yard_per_roll="{4}"
# 							and
# 							warehouse="{5}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll, i.s_warehouse))

# 						# frappe.db.commit()


# @frappe.whitelist()
# def cancel_stock_entry(doc,method):
# 	if doc.purpose == "Material Receipt" :
# 		for i in doc.items :
# 			if i.parent_item :
# 				cek_inventory = frappe.db.sql("""
# 					SELECT
# 					mi.`item_code`
# 					FROM `tabMaster Inventory` mi
# 					WHERE mi.`item_code` = "{}"
# 					""".format(i.parent_item))

# 				if cek_inventory :
# 					cek_data = frappe.db.sql("""
# 						SELECT 
# 						di.`item_code_variant`,
# 						di.`total_roll`,
# 						di.`total_yard`
# 						FROM `tabData Inventory` di
# 						WHERE di.`parent` = "{}"
# 						AND di.`item_code_variant` = "{}"
# 						and di.`yard_per_roll` = "{}"
# 						and di.`warehouse = "{}"
# 					""".format(i.parent_item, i.item_code, i.yard_per_roll, i.t_warehouse))

# 					if cek_data :
# 						current_total_roll = cek_data[0][1]
# 						current_total_yard = cek_data[0][2]

# 						new_total_roll = current_total_roll - (i.qty / i.yard_per_roll)
# 						new_total_yard = current_total_yard - i.qty

# 						frappe.db.sql ("""
# 							update 
# 							`tabData Inventory` 
# 							set 
# 							total_roll="{0}",
# 							total_yard="{1}"
# 							where 
# 							parent="{2}"
# 							AND
# 							item_code_variant="{3}"
# 							AND
# 							yard_per_roll="{4}"
# 							and
# 							warehouse="{5}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll, i.t_warehouse))

# 						# frappe.db.commit()


# 	elif doc.purpose == "Material Issue" :
# 		for i in doc.items :
# 			if i.parent_item :
# 				cek_inventory = frappe.db.sql("""
# 					SELECT
# 					mi.`item_code`
# 					FROM `tabMaster Inventory` mi
# 					WHERE mi.`item_code` = "{}"
# 					""".format(i.parent_item))

# 				if cek_inventory :
# 					cek_data = frappe.db.sql("""
# 						SELECT 
# 						di.`item_code_variant`,
# 						di.`total_roll`,
# 						di.`total_yard`
# 						FROM `tabData Inventory` di
# 						WHERE di.`parent` = "{}"
# 						AND di.`item_code_variant` = "{}"
# 						and di.`yard_per_roll` = "{}"
# 						and di.`warehouse` = "{}"
# 					""".format(i.parent_item, i.item_code, i.yard_per_roll, i.s_warehouse))

# 					if cek_data :
# 						current_total_roll = cek_data[0][1]
# 						current_total_yard = cek_data[0][2]

# 						new_total_roll = current_total_roll + (i.qty / i.yard_per_roll)
# 						new_total_yard = current_total_yard + i.qty

# 						frappe.db.sql ("""
# 							update 
# 							`tabData Inventory` 
# 							set 
# 							total_roll="{0}",
# 							total_yard="{1}"
# 							where 
# 							parent="{2}"
# 							AND
# 							item_code_variant="{3}"
# 							AND
# 							yard_per_roll="{4}"
# 							and warehouse = "{5}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll, i.s_warehouse))

# 						# frappe.db.commit()