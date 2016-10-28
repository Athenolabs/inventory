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

form_grid_templates = {
	"roll_in": "templates/includes/stock_recon.html",
	"roll_out": "templates/includes/stock_recon.html"
}


class StockReconInventory(Document):
	def add_item_roll(self):
		count = 0
		if self.item_code_variant and self.colour and self.yard_atau_meter_per_roll and self.total_roll :
			warehouse = frappe.get_value("Item",self.item_code_variant,"default_warehouse")
			
			if self.type_roll == "Out" :
				if self.group :
					total_roll = frappe.db.sql("""
						SELECT
						di.`total_roll`
						FROM `tabData Inventory` di
						WHERE di.`item_code_variant` = "{}"
						AND di.`colour` = "{}"
						AND di.`yard_atau_meter_per_roll` = "{}"
						AND di.`group` = "{}"
						AND di.`total_roll` >= {}

					""".format(self.item_code_variant, self.colour, self.yard_atau_meter_per_roll, self.group, self.total_roll))
				else :
					total_roll = frappe.db.sql("""
						SELECT
						di.`total_roll`
						FROM `tabData Inventory` di
						WHERE di.`item_code_variant` = "{}"
						AND di.`colour` = "{}"
						AND di.`yard_atau_meter_per_roll` = "{}"
						AND di.`group` IS NULL

					""".format(self.item_code_variant, self.colour, self.yard_atau_meter_per_roll))

				if total_roll :
					count = 0
				else :
					frappe.throw("Item Tidak Ditemukan, ada kemungkinan salah Yard / Colour atau jumlah Roll nya kebanyakan")

			if self.type_roll == "In" :
				if self.roll_in :
					for i in self.roll_in :
						if i.item_code_roll == self.item_code_variant and i.colour == self.colour and i.yard_atau_meter_per_roll == self.yard_atau_meter_per_roll and i.group == self.group :
							count = 1

					if count == 1 :
						for i in self.roll_in :
							if i.item_code_roll == self.item_code_variant and i.colour == self.colour and i.yard_atau_meter_per_roll == self.yard_atau_meter_per_roll and i.group == self.group :
								new_total_roll = i.total_roll
								i.total_roll = new_total_roll + self.total_roll
					else :
						pp_so = self.append('roll_in', {})
						pp_so.item_code_roll = self.item_code_variant
						pp_so.colour = self.colour
						pp_so.yard_atau_meter_per_roll = self.yard_atau_meter_per_roll
						pp_so.group = self.group
						pp_so.total_roll = self.total_roll
						pp_so.rate = self.rate_roll
						pp_so.warehouse = warehouse
						
				else :
					pp_so = self.append('roll_in', {})
					pp_so.item_code_roll = self.item_code_variant
					pp_so.colour = self.colour
					pp_so.yard_atau_meter_per_roll = self.yard_atau_meter_per_roll
					pp_so.group = self.group
					pp_so.total_roll = self.total_roll
					pp_so.rate = self.rate_roll
					pp_so.warehouse = warehouse
					
			elif self.type_roll == "Out" :
				if self.roll_out :
					for i in self.roll_out :
						if i.item_code_roll == self.item_code_variant and i.colour == self.colour and i.yard_atau_meter_per_roll == self.yard_atau_meter_per_roll and i.group == self.group :
							count = 1

					if count == 1 :
						for i in self.roll_out :
							if i.item_code_roll == self.item_code_variant and i.colour == self.colour and i.yard_atau_meter_per_roll == self.yard_atau_meter_per_roll and i.group == self.group :
								new_total_roll = i.total_roll
								i.total_roll = new_total_roll + self.total_roll
					else :
						pp_so = self.append('roll_out', {})
						pp_so.item_code_roll = self.item_code_variant
						pp_so.colour = self.colour
						pp_so.yard_atau_meter_per_roll = self.yard_atau_meter_per_roll
						pp_so.group = self.group
						pp_so.total_roll = self.total_roll
						pp_so.rate = self.rate
						pp_so.warehouse = warehouse
						
				else :
					pp_so = self.append('roll_out', {})
					pp_so.item_code_roll = self.item_code_variant
					pp_so.colour = self.colour
					pp_so.yard_atau_meter_per_roll = self.yard_atau_meter_per_roll
					pp_so.group = self.group
					pp_so.total_roll = self.total_roll
					pp_so.rate = self.rate
					pp_so.warehouse = warehouse
		else :
			frappe.throw("Item Code / Colour / Yard Meter per Roll / Total Roll belum diisi")



	def add_item_pcs(self):
		if self.item_code_pcs and self.qty_pcs :
			
			if self.type_pcs == "Out" :
				total_pcs_from = frappe.db.sql("""
					SELECT
					b.`actual_qty`
					FROM `tabBin` b
					WHERE b.`item_code` = "{}"
				""".format(self.item_code_pcs))

			if total_pcs_from :
				count = 0
			else :
				frappe.throw("Item Tidak Ditemukan, ada kemungkinan jumlah Qty nya kebanyakan")

			if self.type_pcs == "In" :
				if self.stock_recon_inventory_pcs :
					for i in self.stock_recon_inventory_pcs :
						if i.item_code_pcs == self.item_code_pcs  :
							count = 1

					if count == 1 :
						for i in self.stock_recon_inventory_item :
							if i.item_code_pcs == self.item_code_pcs  :
								new_total_roll = i.total_pcs
								i.total_pcs = new_total_roll + self.qty_pcs
							else :
								pp_so = self.append('stock_recon_inventory_pcs', {})
								pp_so.item_code_pcs = self.item_code_pcs
								pp_so.total_pcs = self.qty_pcs
								pp_so.rate = self.rate_pcs
								
				else :
					pp_so = self.append('stock_recon_inventory_pcs', {})
					pp_so.item_code_pcs = self.item_code_pcs
					pp_so.total_pcs = self.qty_pcs
					pp_so.rate = self.rate_pcs

			elif self.type_pcs == "Out" :
				if self.stock_recon_inventory_pcs :
					for i in self.stock_recon_inventory_pcs :
						if i.item_code_pcs == self.item_code_pcs  :
							count = 1

					if count == 1 :
						for i in self.stock_recon_inventory_item :
							if i.item_code_pcs == self.item_code_pcs  :
								new_total_roll = i.total_pcs
								i.total_pcs = new_total_roll + self.qty_pcs
							else :
								pp_so = self.append('stock_recon_inventory_pcs', {})
								pp_so.item_code_pcs = self.item_code_pcs
								pp_so.total_pcs = self.qty_pcs
								pp_so.rate = self.rate_pcs
								
				else :
					pp_so = self.append('stock_recon_inventory_pcs', {})
					pp_so.item_code_pcs = self.item_code_pcs
					pp_so.total_pcs = self.qty_pcs
					pp_so.rate = self.rate_pcs
					

		else :
			frappe.throw("Item Code / Total Pcs belum diisi")
	
	def on_submit(self):
		self.create_stock_entry_on_submit()
		self.add_master_inventory_on_submit()
		self.remove_master_inventory_on_submit()
	
	def on_cancel(self):
		self.cancel_stock_entry_on_cancel()
		self.add_master_inventory_on_cancel()
		self.remove_master_inventory_on_cancel()
	
	
	def cancel_stock_entry_on_cancel(self):
		result = frappe.db.sql(""" SELECT i.`name` FROM `tabStock Entry`i WHERE i.`creating_sri`="{0}" AND i.`docstatus`=1  """.format(self.name), as_list=1)
		for res in result :
			name = res[0]
			se = frappe.get_doc("Stock Entry",name)
			se.cancel()

	def create_stock_entry_on_submit(self):
		
		item_in = {}		
		item_out = {}
		
		for d in self.get("roll_in") :
			if d.item_code_roll in item_in :
				item = item_in[d.item_code_roll]
				
				new_qty = d.total_roll * d.yard_atau_meter_per_roll
				total_qty = item["qty"] + new_qty
				
				new_rate = ((d.rate * new_qty) + (item["rate"] * item["qty"])) / total_qty
				
				item["qty"] = total_qty
				item["rate"] = new_rate
				
				item_in[d.item_code_roll] = item
			else :
				new_item = {}
				new_item["item_code"] = d.item_code_roll
				new_item["warehouse"] = d.warehouse
				new_item["qty"] = d.total_roll * d.yard_atau_meter_per_roll
				new_item["rate"] = d.rate
				
				item_in[d.item_code_roll] = new_item
		
		for d in self.get("pcs_in") :
			new_item = {}
			new_item["item_code"] = d.item_code
			new_item["warehouse"] = d.warehouse
			new_item["qty"] = d.total_roll * d.yard_atau_meter_per_roll
			new_item["rate"] = d.rate
			
			item_in[d.item_code] = item
		
		for d in self.get("roll_out") :
			if d.item_code_roll in item_out :
				item = item_out[d.item_code_roll]
				
				new_qty = d.total_roll * d.yard_atau_meter_per_roll
				total_qty = item["qty"] + new_qty
				
				new_rate = ((d.rate * new_qty) + (item["rate"] * item["qty"])) / total_qty
				
				item["qty"] = total_qty
				item["rate"] = new_rate
				
				item_out[d.item_code_roll] = new_item
				
			else :
				new_item = {}
				new_item["item_code"] = d.item_code_roll
				new_item["warehouse"] = d.warehouse
				new_item["qty"] = d.total_roll * d.yard_atau_meter_per_roll
				new_item["rate"] = d.rate
				
				item_out[d.item_code_roll] = new_item
		
		for d in self.get("pcs_out") :
			new_item = {}
			new_item["item_code"] = d.item_code_roll
			new_item["warehouse"] = d.warehouse
			new_item["qty"] = d.total_roll * d.yard_atau_meter_per_roll
			new_item["rate"] = d.rate
			
			item_out[d.item_code] = item
		
		if len(item_in)>0:
			new_doc = frappe.new_doc("Stock Entry")
			new_doc.purpose = "Material Receipt"
			for key,value in item_in.items() :
				d = new_doc.append("items")
				d.item_code = value["item_code"]
				d.t_warehouse = value["warehouse"]
				d.qty = value["qty"]
				d.basic_rate = value["rate"]
			new_doc.save()
			new_doc.submit()
		if len(item_out)>0:
			new_doc = frappe.new_doc("Stock Entry")
			new_doc.purpose = "Material Issue"
			for key,value in item_out.items() :
				d = new_doc.append("items")
				d.item_code = value["item_code"]
				d.s_warehouse = value["warehouse"]
				d.qty = value["qty"]
				d.basic_rate = value["rate"]
			new_doc.save()
			new_doc.submit()
	
	def add_master_inventory_on_submit(self):
		for d in self.get("roll_in") :
			if d.item_code_roll :
				uom = frappe.get_value("Item",d.item_code_roll,"stock_uom")
				cek_inventory = frappe.db.sql("""
					SELECT
					mi.`item_code`
					FROM `tabMaster Inventory` mi
					WHERE mi.`item_code` = "{}"
					""".format(d.item_code_roll))

				if cek_inventory:
					if d.group :
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
							""".format(d.item_code_roll, d.yard_atau_meter_per_roll, d.warehouse, d.colour, d.group, uom))

						if cek_data :
							current_total_roll = cek_data[0][1]
							current_total_yard = cek_data[0][2]

							new_total_roll = current_total_roll + d.total_roll
							new_total_yard = current_total_yard + (d.total_roll * d.yard_atau_meter_per_roll)

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

								""".format(new_total_roll,new_total_yard,d.item_code_roll,d.yard_atau_meter_per_roll, d.warehouse, d.colour, d.group, uom))

						# frappe.db.commit()

						else :
						
							mi = frappe.get_doc("Master Inventory", d.item_code_roll)
							mi.append("data_inventory", {
								"doctype": "Data Inventory",
								"item_code_variant" : d.item_code_roll,
								"yard_atau_meter_per_roll" : d.yard_atau_meter_per_roll,
								"total_roll" : d.total_roll,
								"total_yard_atau_meter" : d.yard_atau_meter_per_roll * d.total_roll,
								"warehouse" : d.warehouse,
								"colour" : d.colour,
								"group" : d.group,
								"inventory_uom" : uom
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
						""".format(d.item_code_roll, d.yard_atau_meter_per_roll, d.warehouse, d.colour, uom))

						if cek_data :
							current_total_roll = cek_data[0][1]
							current_total_yard = cek_data[0][2]

							new_total_roll = current_total_roll + d.total_roll
							new_total_yard = current_total_yard + d.yard_atau_meter_per_roll * d.total_roll

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

								""".format(new_total_roll,new_total_yard,d.item_code_roll,d.yard_atau_meter_per_roll, d.warehouse, d.colour, uom))

						# frappe.db.commit()

						else :
						
							mi = frappe.get_doc("Master Inventory", d.item_code_roll)
							mi.append("data_inventory", {
								"doctype": "Data Inventory",
								"item_code_variant" : d.item_code_roll,
								"yard_atau_meter_per_roll" : d.yard_atau_meter_per_roll,
								"total_roll" : d.total_roll,
								"total_yard_atau_meter" :d.yard_atau_meter_per_roll * d.total_roll,
								"warehouse" : d.warehouse,
								"colour" : d.colour,
								"inventory_uom" : uom
							})

							mi.flags.ignore_permissions = 1
							mi.save()

				else :
					item = frappe.get_doc("Item", d.item_code_roll)
					mi = frappe.new_doc("Master Inventory")
					mi.update({
						"item_code": item.item_code,
						"item_name": item.item_name	
					})

					if i.group :
						mi.append("data_inventory", {
							"doctype": "Data Inventory",
							"item_code_variant" : d.item_code_roll,
							"yard_atau_meter_per_roll" : d.yard_atau_meter_per_roll,
							"total_roll" : d.total_roll,
							"total_yard_atau_meter" : d.yard_atau_meter_per_roll * d.total_roll,
							"warehouse" : d.warehouse,
							"colour" : d.colour,
							"group" : d.group,
							"inventory_uom" : uom
						})
					else :
						mi.append("data_inventory", {
							"doctype": "Data Inventory",
							"item_code_variant" : d.item_code_roll,
							"yard_atau_meter_per_roll" : d.yard_atau_meter_per_roll,
							"total_roll" : d.total_roll,
							"total_yard_atau_meter" : d.yard_atau_meter_per_roll * d.total_roll,
							"warehouse" : d.warehouse,
							"colour" : d.colour,
							"inventory_uom" : uom
						})

					mi.flags.ignore_permissions = 1
					mi.save()
			
		pass
	
	def remove_master_inventory_on_submit(self) :
		for d in self.get("roll_out") :
			uom = frappe.get_value("Item",d.item_code_roll,"stock_uom")
			if d.group :
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
				""".format(d.item_code_roll, d.yard_atau_meter_per_roll, d.warehouse, d.colour, d.group, uom))

				if cek_data :
					current_total_roll = cek_data[0][1]
					current_total_yard = cek_data[0][2]

					new_total_roll = current_total_roll - d.total_roll
					new_total_yard = current_total_yard - d.total_roll * d.yard_atau_meter_per_roll



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

						""".format(new_total_roll, new_total_yard, d.item_code_roll, d.yard_atau_meter_per_roll, d.warehouse, d.colour, d.group, uom))

			
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
				""".format(d.item_code_roll, d.yard_atau_meter_per_roll, d.warehouse, d.colour, uom))

				if cek_data :
					current_total_roll = cek_data[0][1]
					current_total_yard = cek_data[0][2]

					new_total_roll = current_total_roll - d.total_roll
					new_total_yard = current_total_yard - d.total_roll * d.yard_atau_meter_per_roll

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

						""".format(new_total_roll, new_total_yard, d.item_code_roll, d.yard_atau_meter_per_roll, d.warehouse, d.colour, uom))

						
	def add_master_inventory_on_cancel(self):
		for d in self.get("roll_out") :
			if d.item_code_roll :
				uom = frappe.get_value("Item",d.item_code_roll,"stock_uom")
				cek_inventory = frappe.db.sql("""
					SELECT
					mi.`item_code`
					FROM `tabMaster Inventory` mi
					WHERE mi.`item_code` = "{}"
					""".format(d.item_code_roll))

				if cek_inventory:
					if d.group :
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
							""".format(d.item_code_roll, d.yard_atau_meter_per_roll, d.warehouse, d.colour, d.group, uom))

						if cek_data :
							current_total_roll = cek_data[0][1]
							current_total_yard = cek_data[0][2]

							new_total_roll = current_total_roll + d.total_roll
							new_total_yard = current_total_yard + (d.total_roll * d.yard_atau_meter_per_roll)

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

								""".format(new_total_roll,new_total_yard,d.item_code_roll,d.yard_atau_meter_per_roll, d.warehouse, d.colour, d.group, uom))

						# frappe.db.commit()

						else :
						
							mi = frappe.get_doc("Master Inventory", d.item_code_roll)
							mi.append("data_inventory", {
								"doctype": "Data Inventory",
								"item_code_variant" : d.item_code_roll,
								"yard_atau_meter_per_roll" : d.yard_atau_meter_per_roll,
								"total_roll" : d.total_roll,
								"total_yard_atau_meter" : d.yard_atau_meter_per_roll * d.total_roll,
								"warehouse" : d.warehouse,
								"colour" : d.colour,
								"group" : d.group,
								"inventory_uom" : uom
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
						""".format(d.item_code_roll, d.yard_atau_meter_per_roll, d.warehouse, d.colour, uom))

						if cek_data :
							current_total_roll = cek_data[0][1]
							current_total_yard = cek_data[0][2]

							new_total_roll = current_total_roll + d.total_roll
							new_total_yard = current_total_yard + d.yard_atau_meter_per_roll * d.total_roll

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

								""".format(new_total_roll,new_total_yard,d.item_code_roll,d.yard_atau_meter_per_roll, d.warehouse, d.colour, uom))

						# frappe.db.commit()

						else :
						
							mi = frappe.get_doc("Master Inventory", d.item_code_roll)
							mi.append("data_inventory", {
								"doctype": "Data Inventory",
								"item_code_variant" : d.item_code_roll,
								"yard_atau_meter_per_roll" : d.yard_atau_meter_per_roll,
								"total_roll" : d.total_roll,
								"total_yard_atau_meter" :d.yard_atau_meter_per_roll * d.total_roll,
								"warehouse" : d.warehouse,
								"colour" : d.colour,
								"inventory_uom" : uom
							})

							mi.flags.ignore_permissions = 1
							mi.save()

				else :
					item = frappe.get_doc("Item", d.item_code_roll)
					mi = frappe.new_doc("Master Inventory")
					mi.update({
						"item_code": item.item_code,
						"item_name": item.item_name	
					})

					if i.group :
						mi.append("data_inventory", {
							"doctype": "Data Inventory",
							"item_code_variant" : d.item_code_roll,
							"yard_atau_meter_per_roll" : d.yard_atau_meter_per_roll,
							"total_roll" : d.total_roll,
							"total_yard_atau_meter" : d.yard_atau_meter_per_roll * d.total_roll,
							"warehouse" : d.warehouse,
							"colour" : d.colour,
							"group" : d.group,
							"inventory_uom" : uom
						})
					else :
						mi.append("data_inventory", {
							"doctype": "Data Inventory",
							"item_code_variant" : d.item_code_roll,
							"yard_atau_meter_per_roll" : d.yard_atau_meter_per_roll,
							"total_roll" : d.total_roll,
							"total_yard_atau_meter" : d.yard_atau_meter_per_roll * d.total_roll,
							"warehouse" : d.warehouse,
							"colour" : d.colour,
							"inventory_uom" : uom
						})

					mi.flags.ignore_permissions = 1
					mi.save()
			
		pass
	
	def remove_master_inventory_on_cancel(self) :
		for d in self.get("roll_in") :
			uom = frappe.get_value("Item",d.item_code_roll,"stock_uom")
			if d.group :
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
				""".format(d.item_code_roll, d.yard_atau_meter_per_roll, d.warehouse, d.colour, d.group, uom))

				if cek_data :
					current_total_roll = cek_data[0][1]
					current_total_yard = cek_data[0][2]

					new_total_roll = current_total_roll - d.total_roll
					new_total_yard = current_total_yard - d.total_roll * d.yard_atau_meter_per_roll



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

						""".format(new_total_roll, new_total_yard, d.item_code_roll, d.yard_atau_meter_per_roll, d.warehouse, d.colour, d.group, uom))

			
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
				""".format(d.item_code_roll, d.yard_atau_meter_per_roll, d.warehouse, d.colour, uom))

				if cek_data :
					current_total_roll = cek_data[0][1]
					current_total_yard = cek_data[0][2]

					new_total_roll = current_total_roll - d.total_roll
					new_total_yard = current_total_yard - d.total_roll * d.yard_atau_meter_per_roll

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

						""".format(new_total_roll, new_total_yard, d.item_code_roll, d.yard_atau_meter_per_roll, d.warehouse, d.colour, uom))

	
@frappe.whitelist()
def save_stock_recon_inventory(doc,method):
	pass
	# for i in doc.stock_recon_inventory_item :
	# 	if i.group_from :
	# 		item = frappe.get_doc("Item", i.item_code_roll)
	# 		cek_data = frappe.db.sql("""
	# 			SELECT 
	# 			di.`item_code_variant`,
	# 			di.`total_roll`,
	# 			di.`total_yard_atau_meter`
	# 			FROM `tabData Inventory` di
	# 			WHERE di.`item_codedef create_stock_entry_on_submit(self):_variant` = "{}"
	# 			and di.`yard_atau_meter_per_roll` = "{}"
	# 			and di.`warehouse` = "{}"
	# 			and di.`colour` = "{}"
	# 			and di.`inventory_uom` = "{}"
	# 			and di.`group` = "{}"
	# 		""".format(i.item_code_roll, i.yard_atau_meter_per_roll_from, item.default_warehouse, i.colour, item.stock_uom, i.group_from))
	# 	else :
	# 		item = frappe.get_doc("Item", i.item_code_roll)
	# 		cek_data = frappe.db.sql("""
	# 			SELECT 
	# 			di.`item_code_variant`,
	# 			di.`total_roll`,
	# 			di.`total_yard_atau_meter`
	# 			FROM `tabData Inventory` di
	# 			WHERE di.`item_code_variant` = "{}"
	# 			and di.`yard_atau_meter_per_roll` = "{}"
	# 			and di.`warehouse` = "{}"
	# 			and di.`colour` = "{}"
	# 			and di.`inventory_uom` = "{}"
	# 			and di.`group` is null
				
	# 		""".format(i.item_code_roll, i.yard_atau_meter_per_roll_from, item.default_warehouse, i.colour, item.stock_uom))

	# 	if cek_data :
	# 		count = 0
	# 	else :
	# 		frappe.throw("Itam "+str(i.item_code_roll)+" "+str(i.colour)+" "+str(i.yard_atau_meter_per_roll_from)+" "+str(item.stock_uom)+" tidak ada di dalam inventory")



@frappe.whitelist()
def submit_stock_recon_inventory(doc,method):
	pass
	# pr_doc = frappe.new_doc("Stock Reconciliation")
	# pr_doc.update({
	# 	"posting_date" : doc.posting_date,
	# 	"psoting_time" : doc.psoting_time,
	# 	"stock_recon_inventory" : doc.name
	# })

	# get_data_roll = frappe.db.sql("""
	# 	SELECT 
	# 	srii.`item_code_roll`,
	# 	SUM(srii.`total_roll_to` * srii.`yard_atau_meter_per_roll_from`)
	# 	FROM `tabStock Recon Inventory Item` srii
	# 	WHERE srii.`parent` = "{}"
	# 	GROUP BY srii.`item_code_roll`
	# """.format(doc.name))


	# get_data_pcs = frappe.db.sql("""
	# 	SELECT 
	# 	srii.`item_code_pcs`,
	# 	SUM(srii.`total_pcs_to`)
	# 	FROM `tabStock Recon Inventory Pcs` srii
	# 	WHERE srii.`parent` = "{}"
	# 	GROUP BY srii.`item_code_pcs`
	# """.format(doc.name))

	# if get_data_roll :
	# 	for i in get_data_roll :
	# 		warehouse = frappe.get_doc("Item",i[0]).default_warehouse
	# 		pr_doc.append("items", {
	# 			"item_code": i[0],
	# 			"qty" : i[1],
	# 			"warehouse": warehouse
	# 		})

	# if get_data_pcs :
	# 	for i in get_data_pcs :
	# 		warehouse = frappe.get_doc("Item",i[0]).default_warehouse
	# 		pr_doc.append("items", {
	# 			"item_code": i[0],
	# 			"qty" : i[1],
	# 			"warehouse": warehouse
	# 		})

	# pr_doc.flags.ignore_permissions = 1
	# pr_doc.save()


	# if doc.stock_recon_inventory_item :
	# 	for i in doc.stock_recon_inventory_item :
	# 		total_yard_atau_meter = i.yard_atau_meter_per_roll_from * i.total_roll_to
	# 		total_roll = i.total_roll_to
	# 		item_code_variant = i.item_code_roll
	# 		colour = i.colour
	# 		yard_atau_meter_per_roll = i.yard_atau_meter_per_roll_from
	# 		warehouse = frappe.get_doc("Item",i.item_code_roll).default_warehouse
	# 		inventory_uom = frappe.get_doc("Item",i.item_code_roll).stock_uom
	# 		frappe.db.sql ("""
	# 			update 
	# 			`tabData Inventory` 
	# 			set 
	# 			total_yard_atau_meter="{0}",
	# 			total_roll="{1}"
	# 			where 
	# 			item_code_variant="{2}"
	# 			and
	# 			colour="{3}"
	# 			and
	# 			yard_atau_meter_per_roll = "{4}"
	# 			and 
	# 			warehouse = "{5}"
	# 			and inventory_uom = "{6}"
				
	# 			""".format(total_yard_atau_meter,total_roll,item_code_variant,colour,yard_atau_meter_per_roll,warehouse,inventory_uom))




@frappe.whitelist()
def cancel_stock_recon_inventory(doc,method):
	pass
	# if doc.stock_recon_inventory_item :
	# 	for i in doc.stock_recon_inventory_item :
	# 		total_yard_atau_meter = i.yard_atau_meter_per_roll_from * i.total_roll_from
	# 		total_roll = i.total_roll_from
	# 		item_code_variant = i.item_code_roll
	# 		colour = i.colour
	# 		yard_atau_meter_per_roll = i.yard_atau_meter_per_roll_from
	# 		warehouse = frappe.get_doc("Item",i.item_code_roll).default_warehouse
	# 		inventory_uom = frappe.get_doc("Item",i.item_code_roll).stock_uom
	# 		frappe.db.sql ("""
	# 			update 
	# 			`tabData Inventory` 
	# 			set 
	# 			total_yard_atau_meter="{0}",
	# 			total_roll="{1}"
	# 			where 
	# 			item_code_variant="{2}"
	# 			and
	# 			colour="{3}"
	# 			and
	# 			yard_atau_meter_per_roll = "{4}"
	# 			and 
	# 			warehouse = "{5}"
	# 			and inventory_uom = "{6}"
				
	# 			""".format(total_yard_atau_meter,total_roll,item_code_variant,colour,yard_atau_meter_per_roll,warehouse,inventory_uom))