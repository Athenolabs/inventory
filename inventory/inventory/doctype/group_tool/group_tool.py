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

class GroupTool(Document):

	# split group
	def get_group_code(self):
		if self.type_tool == "Split Group" :
			if self.group_code_other :
				get_data_group = frappe.db.sql("""
					SELECT
					gi.`group_code`,
					gi.`uom`,

					dg.`item_code_variant`,
					dg.`item_name`,
					dg.`parent_item`,
					dg.`colour`,
					dg.`yard_atau_meter`,
					dg.`warehouse`,
					dg.`inventory_uom`,
					dg.`total_qty_roll`

					FROM `tabGroup Item` gi
					JOIN `tabData Group` dg
					ON gi.`name` = dg.`parent`
					WHERE gi.`group_code` = "{}"
					AND dg.`is_used` = 0
					order by dg.`idx`, dg.`colour`

				""".format(self.group_code_other))

				if get_data_group :
					for dg in get_data_group :
							
						pp_so = self.append('split_group_temp', {})
						pp_so.colour = dg[5]
						pp_so.total_qty_roll = dg[9]
						pp_so.yard_atau_meter = dg[6]
							
				else :
					frappe.throw("Group Tidak Active / Tidak Memiliki Item")
			else :
				frappe.throw("Group Item belum dipilih")


	# split group
	def get_split(self):
		if self.type_tool == "Split Group" :
			if self.group_code_split :
				get_data_group = frappe.db.sql("""
					SELECT
					gi.`group_code`,
					gi.`uom`,

					dg.`item_code_variant`,
					dg.`item_name`,
					dg.`parent_item`,
					dg.`colour`,
					dg.`yard_atau_meter`,
					dg.`warehouse`,
					dg.`inventory_uom`,
					dg.`total_qty_roll`

					FROM `tabGroup Item` gi
					JOIN `tabData Group` dg
					ON gi.`name` = dg.`parent`
					WHERE gi.`group_code` = "{}"
					AND dg.`is_used` = 0
					order by dg.`idx`, dg.`colour`

				""".format(self.group_code_split))

				if get_data_group :
					for dg in get_data_group :
							
						pp_so = self.append('split_group_item', {})
						pp_so.colour = dg[5]
						pp_so.total_qty_roll = dg[9]
						pp_so.yard_atau_meter = dg[6]
							
				else :
					frappe.throw("Group Tidak Active / Tidak Memiliki Item")
			else :
				frappe.throw("Group Item belum dipilih")




	# add group
	def add_add(self):
		if self.type_tool == "Add Group" :
			if self.item_code_add :
				if self.colour_add and self.yard_atau_meter_per_roll_add and self.qty_add :

					check_inventory = 0

					cek_group = frappe.db.sql("""
						SELECT
						di.`item_code_variant`,
						di.`yard_atau_meter_per_roll`,
						di.`colour`,
						di.`total_roll`
						FROM `tabData Inventory` di
						WHERE di.`parent` = "{}"
						AND di.`colour` = "{}"
						AND di.`yard_atau_meter_per_roll` = "{}"
						AND di.`total_roll` >= "{}"
						AND di.`group` IS NULL
					""".format(self.item_code_add, self.colour_add, self.yard_atau_meter_per_roll_add, self.qty_add))

					if cek_group :
						check_inventory = 0
					else :
						frappe.throw("Colour " + str(self.colour_add) +", Yard/Meter "+ str(self.yard_atau_meter_per_roll_add) +" tidak ada di Inventory atau Qty "+ str(self.qty_add) +" nya terlalu besar daripada di Inventory")

					if check_inventory == 0 :

						item = frappe.get_doc("Item",self.item_code_add)

						pp_so = self.append('new_data_group_add', {})
						pp_so.item_code_variant = self.item_code_add
						pp_so.item_name = item.item_name
						pp_so.colour = self.colour_add
						pp_so.yard_atau_meter = self.yard_atau_meter_per_roll_add
						pp_so.warehouse = item.default_warehouse
						pp_so.inventory_uom = item.stock_uom
						pp_so.total_qty_meter_atau_yard = self.yard_atau_meter_per_roll_add * self.qty_add
						pp_so.total_qty_roll = self.qty_add

						self.colour_add = ""
						self.yard_atau_meter_per_roll_add = 0
						self.qty_add = 1		

				else :
					frappe.throw("Colour / Yard Meter / Qty tidak ada")
			else :
				frappe.throw("Item Code tidak ada")







# submit add group
@frappe.whitelist()
def submit_group_tool(doc,method):

	# split group no group
	if doc.type_tool == "Split Group" and doc.split_type == "No Group":
		if doc.group_code_split :
			if doc.split_group_item :
				item = frappe.get_doc("Item", doc.group_code_split.split(".")[0])
				for i in doc.split_group_item :
					
					# mengurangi data di inventory sesuai grup asal
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
					""".format(item.item_code, i.yard_atau_meter, item.default_warehouse, i.colour, doc.group_code_split, item.stock_uom))

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
							AND di.`group` = "{6}"
							AND di.`inventory_uom` = "{7}"

							 """.format(new_total_roll,new_total_yard,item.item_code, i.yard_atau_meter, item.default_warehouse, i.colour, doc.group_code_split, item.stock_uom))


					# menambahkan data ke inventory dari grup asal
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
					""".format(item.item_code, i.yard_atau_meter, item.default_warehouse, i.colour, item.stock_uom))

					if cek_data :
						current_total_roll = cek_data[0][1]
						current_total_yard = cek_data[0][2]

						new_total_roll = current_total_roll + i.total_qty_roll
						new_total_yard = current_total_yard + (i.yard_atau_meter * i.total_qty_roll)

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
							AND di.`group` is null
							AND di.`inventory_uom` = "{6}"

							 """.format(new_total_roll,new_total_yard,item.item_code, i.yard_atau_meter, item.default_warehouse, i.colour, item.stock_uom))

					else :
						
						mi = frappe.get_doc("Master Inventory", item.item_code)
						mi.append("data_inventory", {
							"doctype": "Data Inventory",
							"item_code_variant" : item.item_code,
							"yard_atau_meter_per_roll" : i.yard_atau_meter,
							"total_roll" : i.total_qty_roll,
							"total_yard_atau_meter" : i.yard_atau_meter * i.total_qty_roll,
							"warehouse" : item.default_warehouse,
							"colour" : i.colour,
							"inventory_uom" : item.stock_uom
						})

						mi.flags.ignore_permissions = 1
						mi.save()


	# split group no group
	if doc.type_tool == "Split Group" and doc.split_type == "To Other Group":
		if doc.group_code_other :
			if doc.split_group_item :
				item = frappe.get_doc("Item", doc.group_code_split.split(".")[0])
				for i in split_group_item :
					count = 0
					get_data_group = frappe.db.sql("""
						SELECT
						gi.`group_code`,
						gi.`uom`,

						dg.`item_code_variant`,
						dg.`item_name`,
						dg.`parent_item`,
						dg.`colour`,
						dg.`yard_atau_meter`,
						dg.`warehouse`,
						dg.`inventory_uom`,
						dg.`total_qty_roll`

						FROM `tabGroup Item` gi
						JOIN `tabData Group` dg
						ON gi.`name` = dg.`parent`
						WHERE gi.`group_code` = "{}"
						AND dg.`colour` = "{}"
						AND dg.`yard_atau-meter` = "{}"
						AND dg.`is_used` = 0
						order by dg.`idx`, dg.`colour`

					""".format(doc.group_code_split, i.colour, i.yard_atau_meter))

					if get_data_group :
						count = 0 
					else :
						frappe.throw("Colour "+i.colour+" dan Yard/Meter "+str(i.yard_atau_meter)+" sudah di gunakan")

				for i in doc.split_group_item :

					# menambahkan data di dalam group
					mi = frappe.get_doc("Group Item", new_group)
					
					mi.append("data_group", {
						"doctype": "Data Group",
						"item_code_variant" : doc.group_code_split.split(".")[0],
						"colour" : i.colour,
						"yard_atau_meter" : i.yard_atau_meter,
						"item_name" : item.item_name,
						"warehouse" : item.default_warehouse,
						"inventory_uom" : item.stock_uom,
						"total_qty_meter_atau_yard" : i.yard_atau_meter * i.total_qty_roll,
						"total_qty_roll" : i.total_qty_roll
					})
					mi.flags.ignore_permissions = 1
					mi.save()


					# menambahkan data ke inventory dari grup baru
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
					""".format(doc.group_code_split.split(".")[0], i.yard_atau_meter, item.default_warehouse, i.colour, new_group, item.stock_uom))

					if cek_data :
						current_total_roll = cek_data[0][1]
						current_total_yard = cek_data[0][2]

						new_total_roll = current_total_roll + i.total_qty_roll
						new_total_yard = current_total_yard + (i.yard_atau_meter * i.total_qty_roll)

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

							 """.format(new_total_roll,new_total_yard,doc.group_code_split.split(".")[0], i.yard_atau_meter, item.default_warehouse, i.colour, new_group, item.stock_uom))

					else :
						
						mi = frappe.get_doc("Master Inventory", doc.group_code_split.split(".")[0])
						mi.append("data_inventory", {
							"doctype": "Data Inventory",
							"item_code_variant" : doc.group_code_split.split(".")[0],
							"yard_atau_meter_per_roll" : i.yard_atau_meter,
							"total_roll" : i.total_qty_roll,
							"total_yard_atau_meter" : i.yard_atau_meter * i.total_qty_roll,
							"warehouse" : item.default_warehouse,
							"colour" : i.colour,
							"inventory_uom" : item.stock_uom,
							"group" : new_group
						})

						mi.flags.ignore_permissions = 1
						mi.save()


					# mengurangi data di dalam inventory
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
						and di.`group` = "{}"
					""".format(doc.group_code_split.split(".")[0], i.yard_atau_meter, item.default_warehouse, i.colour, item.stock_uom, doc.group_code_split))

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
							and di.`group` = "{}"

						""".format(new_total_roll, new_total_yard, doc.group_code_split.split(".")[0], i.yard_atau_meter, item.default_warehouse, i.colour, item.stock_uom, doc.group_code_split))





	# split group new group
	if doc.type_tool == "Split Group" and doc.split_type == "New Group":
		if doc.new_group_code :
			if doc.split_group_item :
				# validasi setelah di save masih apa ada item yang sudah di gunakan atau tidak
				for i in split_group_item :
					count = 0
					get_data_group = frappe.db.sql("""
						SELECT
						gi.`group_code`,
						gi.`uom`,
						dg.`item_code_variant`,
						dg.`item_name`,
						dg.`parent_item`,
						dg.`colour`,
						dg.`yard_atau_meter`,
						dg.`warehouse`,
						dg.`inventory_uom`,
						dg.`total_qty_roll`
						FROM `tabGroup Item` gi
						JOIN `tabData Group` dg
						ON gi.`name` = dg.`parent`
						WHERE gi.`group_code` = "{}"
						AND dg.`colour` = "{}"
						AND dg.`yard_atau-meter` = "{}"
						AND dg.`is_used` = 0
						order by dg.`idx`, dg.`colour`
					""".format(doc.group_code_split, i.colour, i.yard_atau_meter))
					if get_data_group :
						count = 0 
					else :
						frappe.throw("Colour "+i.colour+" dan Yard/Meter "+str(i.yard_atau_meter)+" sudah di gunakan")



				new_group = doc.group_code_split.split(".")[0]+"."+doc.new_group_code
				item = frappe.get_doc("Item", doc.group_code_split.split(".")[0])
				cek_new_group = frappe.db.sql("""
					SELECT
					gi.`group_code`
					FROM `tabGroup Item` gi
					WHERE gi.`group_code` = "{}"
				""".format(new_group))

				if cek_new_group :
					frappe.throw("Group sudah ada, tidak bisa menggunakan New Group Code")
				else :
					mi = frappe.new_doc("Group Item")
					mi.update({
						"group_code": new_group,
						"group_name": new_group,
						"uom" : item.stock_uom,
						"keterangan_group" : doc.keterangan_group,
						"is_active": 1		
					})
					mi.flags.ignore_permissions = 1
					mi.save()

					for i in doc.split_group_item :

						# menambahkan data di dalam group
						mi = frappe.get_doc("Group Item", new_group)
						
						mi.append("data_group", {
							"doctype": "Data Group",
							"item_code_variant" : doc.group_code_split.split(".")[0],
							"colour" : i.colour,
							"yard_atau_meter" : i.yard_atau_meter,
							"item_name" : item.item_name,
							"warehouse" : item.default_warehouse,
							"inventory_uom" : item.stock_uom,
							"total_qty_meter_atau_yard" : i.yard_atau_meter * i.total_qty_roll,
							"total_qty_roll" : i.total_qty_roll
						})
						mi.flags.ignore_permissions = 1
						mi.save()

						# menambahkan data ke inventory dari grup baru
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
						""".format(doc.group_code_split.split(".")[0], i.yard_atau_meter, item.default_warehouse, i.colour, new_group, item.stock_uom))

						if cek_data :
							current_total_roll = cek_data[0][1]
							current_total_yard = cek_data[0][2]

							new_total_roll = current_total_roll + i.total_qty_roll
							new_total_yard = current_total_yard + (i.yard_atau_meter * i.total_qty_roll)

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

								 """.format(new_total_roll,new_total_yard,doc.group_code_split.split(".")[0], i.yard_atau_meter, item.default_warehouse, i.colour, new_group, item.stock_uom))

						else :
							
							mi = frappe.get_doc("Master Inventory", doc.group_code_split.split(".")[0])
							mi.append("data_inventory", {
								"doctype": "Data Inventory",
								"item_code_variant" : doc.group_code_split.split(".")[0],
								"yard_atau_meter_per_roll" : i.yard_atau_meter,
								"total_roll" : i.total_qty_roll,
								"total_yard_atau_meter" : i.yard_atau_meter * i.total_qty_roll,
								"warehouse" : item.default_warehouse,
								"colour" : i.colour,
								"inventory_uom" : item.stock_uom,
								"group" : new_group
							})

							mi.flags.ignore_permissions = 1
							mi.save()


						# mengurangi data di dalam inventory
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
						""".format(doc.group_code_split.split(".")[0], i.yard_atau_meter, item.default_warehouse, i.colour, item.stock_uom))

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
								and di.`group` is null

							""".format(new_total_roll, new_total_yard, doc.group_code_split.split(".")[0], i.yard_atau_meter, item.default_warehouse, i.colour, item.stock_uom))
			else :
				frappe.throw("Group Item tidak ada")
		else :
			frappe.throw("New Group Code belum ada isinya")


	# add group
	if doc.type_tool == "Add Group" :
		if doc.item_code_add and doc.group_code_add :
			if doc.new_data_group_add :
				check_inventory = 0
				# dicek dulu di inventory ada apa ndak
				for i in doc.new_data_group_add :
					cek_group = frappe.db.sql("""
						SELECT
						di.`item_code_variant`,
						di.`yard_atau_meter_per_roll`,
						di.`colour`,
						di.`total_roll`
						FROM `tabData Inventory` di
						WHERE di.`parent` = "{}"
						AND di.`colour` = "{}"
						AND di.`yard_atau_meter_per_roll` = "{}"
						AND di.`total_roll` >= "{}"
						AND di.`group` IS NULL
					""".format(doc.item_code_add, i.colour, i.yard_atau_meter, i.total_qty_roll))

					if cek_group :
						check_inventory = 0
					else :
						frappe.throw("Colour " + str(i.colour) +", Yard/Meter "+ str(i.yard_atau_meter) +" tidak ada di Inventory atau Qty "+ str(i.total_qty_roll) +" nya terlalu besar daripada di Inventory")

				if check_inventory == 0 :
					meow = 0
					keterangan_group = ""
					group_code = str(doc.item_code_add) + "." + str(doc.group_code_add)
					item = frappe.get_doc("Item",doc.item_code_add)

					if doc.keterangan_group_add : 
						keterangan_group = doc.keterangan_group_add

					cek_group = frappe.db.sql("""
						SELECT
						mi.`group_code`
						FROM `tabGroup Item` mi
						WHERE mi.`group_code` = "{}"
					""".format(group_code))

					if cek_group :
						for i in doc.new_data_group_add :

							# menambahkan data di dalam group
							mi = frappe.get_doc("Group Item", group_code)
							
							mi.append("data_group", {
								"doctype": "Data Group",
								"item_code_variant" : doc.item_code_add,
								"colour" : i.colour,
								"yard_atau_meter" : i.yard_atau_meter,
								"item_name" : item.item_name,
								"warehouse" : item.default_warehouse,
								"inventory_uom" : item.stock_uom,
								"total_qty_meter_atau_yard" : i.yard_atau_meter*i.total_qty_roll,
								"total_qty_roll" : i.total_qty_roll
							})
							mi.flags.ignore_permissions = 1
							mi.save()


							# menambahkan data ke inventory dari grup baru
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
							""".format(doc.group_code_split.split(".")[0], i.yard_atau_meter, item.default_warehouse, i.colour, new_group, item.stock_uom))

							if cek_data :
								current_total_roll = cek_data[0][1]
								current_total_yard = cek_data[0][2]

								new_total_roll = current_total_roll + i.total_qty_roll
								new_total_yard = current_total_yard + (i.yard_atau_meter * i.total_qty_roll)

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

									 """.format(new_total_roll,new_total_yard,doc.group_code_split.split(".")[0], i.yard_atau_meter, item.default_warehouse, i.colour, new_group, item.stock_uom))

							else :
								
								mi = frappe.get_doc("Master Inventory", doc.group_code_split.split(".")[0])
								mi.append("data_inventory", {
									"doctype": "Data Inventory",
									"item_code_variant" : doc.group_code_split.split(".")[0],
									"yard_atau_meter_per_roll" : i.yard_atau_meter,
									"total_roll" : i.total_qty_roll,
									"total_yard_atau_meter" : i.yard_atau_meter * i.total_qty_roll,
									"warehouse" : item.default_warehouse,
									"colour" : i.colour,
									"inventory_uom" : item.stock_uom,
									"group" : new_group
								})

								mi.flags.ignore_permissions = 1
								mi.save()


							# mengurangi data di dalam inventory
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
							""".format(doc.item_code_add, i.yard_atau_meter, item.default_warehouse, i.colour, item.stock_uom))

							if cek_data :
								current_total_roll = cek_data[0][1]
								current_total_yard = cek_data[0][2]

								new_total_roll = current_total_roll - i.total_qty_roll
								new_total_yard = current_total_yard - (i.yard_atau_meter*i.total_qty_roll)

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

								""".format(new_total_roll, new_total_yard, doc.item_code_add, i.yard_atau_meter, item.default_warehouse, i.colour, item.stock_uom))

						msgprint("Item telah ditambahkan kedalam Group")

					else :
						mi = frappe.new_doc("Group Item")
						mi.update({
							"group_code": group_code,
							"group_name": group_code,
							"uom" : item.stock_uom,
							"keterangan_group" : keterangan_group,
							"is_active": 1		
						})
						mi.flags.ignore_permissions = 1
						mi.save()

						for i in doc.new_data_group_add :

							# menambahkan data di dalam group
							mi = frappe.get_doc("Group Item", group_code)
							
							mi.append("data_group", {
								"doctype": "Data Group",
								"item_code_variant" : doc.item_code_add,
								"colour" : i.colour,
								"yard_atau_meter" : i.yard_atau_meter,
								"item_name" : item.item_name,
								"warehouse" : item.default_warehouse,
								"inventory_uom" : item.stock_uom,
								"total_qty_meter_atau_yard" : i.yard_atau_meter*i.total_qty_roll,
								"total_qty_roll" : i.total_qty_roll
							})
							mi.flags.ignore_permissions = 1
							mi.save()


							# menambahkan data ke inventory dari grup baru
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
							""".format(doc.group_code_split.split(".")[0], i.yard_atau_meter, item.default_warehouse, i.colour, group_code, item.stock_uom))

							if cek_data :
								current_total_roll = cek_data[0][1]
								current_total_yard = cek_data[0][2]

								new_total_roll = current_total_roll + i.total_qty_roll
								new_total_yard = current_total_yard + (i.yard_atau_meter * i.total_qty_roll)

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

									 """.format(new_total_roll,new_total_yard,doc.group_code_split.split(".")[0], i.yard_atau_meter, item.default_warehouse, i.colour, group_code, item.stock_uom))

							else :
								
								mi = frappe.get_doc("Master Inventory", doc.group_code_split.split(".")[0])
								mi.append("data_inventory", {
									"doctype": "Data Inventory",
									"item_code_variant" : doc.group_code_split.split(".")[0],
									"yard_atau_meter_per_roll" : i.yard_atau_meter,
									"total_roll" : i.total_qty_roll,
									"total_yard_atau_meter" : i.yard_atau_meter * i.total_qty_roll,
									"warehouse" : item.default_warehouse,
									"colour" : i.colour,
									"inventory_uom" : item.stock_uom,
									"group" : group_code
								})

								mi.flags.ignore_permissions = 1
								mi.save()


							# mengurangi data di dalam inventory
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
							""".format(doc.item_code_add, i.yard_atau_meter, item.default_warehouse, i.colour, item.stock_uom))

							if cek_data :
								current_total_roll = cek_data[0][1]
								current_total_yard = cek_data[0][2]

								new_total_roll = current_total_roll - i.total_qty_roll
								new_total_yard = current_total_yard - (i.yard_atau_meter*i.total_qty_roll)

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

								""".format(new_total_roll, new_total_yard, doc.item_code_add, i.yard_atau_meter, item.default_warehouse, i.colour, item.stock_uom))
				
				msgprint("Group baru telah dibuat")
			else :
				frappe.throw("Tabel Item tidak ada isinya")
		else :
			frappe.throw("Item Code / Group Code tidak ada")