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

form_grid_templates = {
	"packing_list_data": "templates/includes/item_grid_packing_list.html",
	"summary_purchase_order": "templates/includes/tabel_purchase_order.html"

}

class PackingListReceipt(Document):
	def add_item(self):
		count = 0

		if self.item_code_variant_depan and self.yard_atau_meter and self.colour and self.warehouse :
			master_item = frappe.get_doc("Item", self.item_code_variant_depan)
			parent_item = master_item.variant_of
			item_name = master_item.item_name
			if self.packing_list_data :
				for i in self.packing_list_data :
					if self.group_prefix and self.group_code :
						if i.item_code_variant == self.item_code_variant_depan and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour and i.group == (self.group_prefix+"."+self.group_code) and i.inventory_uom == self.inventory_uom :
							count = 1
					else :
						if i.item_code_variant == self.item_code_variant_depan and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour and i.inventory_uom == self.inventory_uom and i.group == "" :
							count = 1

				if count == 1 :
					for i in self.packing_list_data :
						if self.group_prefix and self.group_code :
							if i.item_code_variant == self.item_code_variant_depan and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour and i.group == (self.group_prefix+"."+self.group_code) and i.inventory_uom == self.inventory_uom :
								new_total_yard_atau_meter = i.total_yard_atau_meter
								new_total_roll = i.total_roll
								i.total_roll = new_total_roll + self.qty_roll
								i.total_yard_atau_meter = new_total_yard_atau_meter + (self.yard_atau_meter * self.qty_roll)
						else :
							if i.item_code_variant == self.item_code_variant_depan and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour and i.inventory_uom == self.inventory_uom and i.group == "" :
								new_total_yard_atau_meter = i.total_yard_atau_meter
								new_total_roll = i.total_roll
								i.total_roll = new_total_roll + self.qty_roll
								i.total_yard_atau_meter = new_total_yard_atau_meter + (self.yard_atau_meter * self.qty_roll)
						
				else :
					if self.group_prefix and self.group_code :
						pp_so = self.append('packing_list_data', {})
						pp_so.item_code_variant = self.item_code_variant_depan
						pp_so.yard_atau_meter_per_roll = self.yard_atau_meter
						pp_so.total_yard_atau_meter = (self.yard_atau_meter * self.qty_roll)
						pp_so.total_roll = self.qty_roll
						pp_so.group = self.group_prefix+"."+self.group_code
						pp_so.parent_item = parent_item
						pp_so.item_name = item_name
						pp_so.warehouse = self.warehouse
						pp_so.colour = self.colour
						pp_so.inventory_uom = self.inventory_uom
						pp_so.keterangan_group = self.keterangan_group
						
					else :
						pp_so = self.append('packing_list_data', {})
						pp_so.item_code_variant = self.item_code_variant_depan
						pp_so.yard_atau_meter_per_roll = self.yard_atau_meter
						pp_so.total_yard_atau_meter = (self.yard_atau_meter * self.qty_roll)
						pp_so.total_roll = self.qty_roll
						pp_so.parent_item = parent_item
						pp_so.item_name = item_name
						pp_so.warehouse = self.warehouse
						pp_so.colour = self.colour
						pp_so.inventory_uom = self.inventory_uom

			else :
				if self.group_prefix and self.group_code :
					pp_so = self.append('packing_list_data', {})
					pp_so.item_code_variant = self.item_code_variant_depan
					pp_so.yard_atau_meter_per_roll = self.yard_atau_meter
					pp_so.total_yard_atau_meter = (self.yard_atau_meter * self.qty_roll)
					pp_so.total_roll = self.qty_roll
					pp_so.group = self.group_prefix+"."+self.group_code
					pp_so.parent_item = parent_item
					pp_so.item_name = item_name
					pp_so.warehouse = self.warehouse
					pp_so.colour = self.colour
					pp_so.inventory_uom = self.inventory_uom
					pp_so.keterangan_group = self.keterangan_group
					
				else :
					pp_so = self.append('packing_list_data', {})
					pp_so.item_code_variant = self.item_code_variant_depan
					pp_so.yard_atau_meter_per_roll = self.yard_atau_meter
					pp_so.total_yard_atau_meter = (self.yard_atau_meter * self.qty_roll)
					pp_so.total_roll = self.qty_roll
					pp_so.parent_item = parent_item
					pp_so.item_name = item_name
					pp_so.warehouse = self.warehouse
					pp_so.colour = self.colour
					pp_so.inventory_uom = self.inventory_uom


			
			self.yard_atau_meter = 0
			self.qty_roll = 1
			self.colour = ""
			
			
		else :
			frappe.throw("Item Code / Colour / Warehouse / Yard / Meter tidak terisi")


	def add_pcs(self):
		count = 0

		if self.item_code_pcs and self.warehouse_pcs :
			parent_item = frappe.get_doc("Item", self.item_code_pcs).variant_of
			item_name = frappe.get_doc("Item", self.item_code_pcs).item_name
			if self.packing_list_data_pcs :
				for i in self.packing_list_data_pcs :
					if i.item_code_pcs == self.item_code_pcs and i.warehouse_pcs == self.warehouse_pcs :
						count = 1

				if count == 1 :
					for i in self.packing_list_data_pcs :
						if i.item_code_pcs == self.item_code_pcs and i.warehouse_pcs == self.warehouse_pcs :
							new_total_pcs = i.total_pcs
							i.total_pcs = new_total_pcs + self.qty_pcs
				else :
					pp_so = self.append('packing_list_data_pcs', {})
					pp_so.item_code_pcs = self.item_code_pcs
					pp_so.total_pcs = self.qty_pcs
					pp_so.parent_item_pcs = parent_item
					pp_so.item_name_pcs = item_name
					pp_so.warehouse_pcs = self.warehouse_pcs
					pp_so.uom_pcs = self.uom_pcs

			else :
				pp_so = self.append('packing_list_data_pcs', {})
				pp_so.item_code_pcs = self.item_code_pcs
				pp_so.total_pcs = self.qty_pcs
				pp_so.parent_item_pcs = parent_item
				pp_so.item_name_pcs = item_name
				pp_so.warehouse_pcs = self.warehouse_pcs
				pp_so.uom_pcs = self.uom_pcs


			
			self.qty_pcs = 0
			
		else :
			frappe.throw("Item Code / Warehouse tidak terisi")




@frappe.whitelist()
def submit_packing_list_receipt(doc,method):
	# packing list data yard/meter
	if doc.packing_list_data :
		temp_gruop = []
		g = ""
		c = 0
		panjang = len(doc.packing_list_data)
		for data in doc.packing_list_data :
			if data.group :
				if data.group == g :
					g = data.group
					c = c + 1
					
				else :
					temp_gruop.append([data.group, data.inventory_uom, data.keterangan_group])
					g = data.group
					c = c + 1
					if panjang == c :
						temp_gruop.append([data.group, data.inventory_uom, data.keterangan_group])


		for t in temp_gruop :
			meow = 0
			cek_group = frappe.db.sql("""
				SELECT
				mi.`group_code`
				FROM `tabGroup Item` mi
				WHERE mi.`group_code` = "{}"
				""".format(t[0]))

			if cek_group :
				meow = 0
			else :
				mi = frappe.new_doc("Group Item")
				mi.update({
					"group_code": t[0],
					"group_name": t[0],
					"uom" : t[1],
					"keterangan_group" : t[2],
					"is_active": 1,
					"packing_list_receipt" : doc.name		
				})
				mi.flags.ignore_permissions = 1
				mi.save()


		count = 0
		skip = 0
		temp_group = []
		temp_name_group = ""
		for data in doc.packing_list_data :
			if data.group :
				if data.group == temp_name_group :
					skip = 0
					temp_name_group = data.group
				else :
					temp_group.append(data.group)
					temp_name_group = data.group

				cek_group = frappe.db.sql("""
					SELECT
					mi.`group_code`
					FROM `tabGroup Item` mi
					WHERE mi.`group_code` = "{}"
					AND mi.`uom` = "{}"
					""".format(data.group, data.inventory_uom))

				if cek_group :
					cek_data = frappe.db.sql("""
						SELECT 
						di.`item_code_variant`
						FROM `tabData Group` di
						WHERE di.`item_code_variant` = "{}"

						and di.`yard_atau_meter` = "{}"
						and di.`colour` = "{}"
						and di.`parent` = "{}"
					""".format(data.item_code_variant, data.yard_atau_meter_per_roll, data.colour, data.group))

					if cek_data :
						count = 0
					else :
						mi = frappe.get_doc("Group Item", data.group)
						
						mi.append("data_group", {
							"doctype": "Data Group",
							"item_code_variant" : data.item_code_variant,
							"colour" : data.colour,
							"yard_atau_meter" : data.yard_atau_meter_per_roll,
							"parent_item" : data.parent_item,
							"item_name" : data.item_name,
							"warehouse" : data.warehouse,
							"inventory_uom" : data.inventory_uom,

							"total_qty_meter_atau_yard" : data.total_yard_atau_meter,
							"total_qty_roll" : data.total_roll,

							"packing_list_receipt" : doc.name
						})
						mi.flags.ignore_permissions = 1
						mi.save()

		# for i in temp_gruop :
		# 	mi = frappe.get_doc("Group Item", i[0])
		# 	mi.flags.ignore_permissions = 1
		# 	mi.submit()

		# for data in doc.packing_list_data :
		# 	if data.group :
		# 		if temp_group == data.group :
		# 			temp_group = data.group
		# 		else :
		# 			temp_group = data.group
		# 			mi = frappe.get_doc("Group Item", temp_group)
		# 			mi.flags.ignore_permissions = 1
		# 			mi.submit()
					

				# else :
				# 	mi = frappe.new_doc("Group Item")
				# 	mi.update({
				# 		"group_code": data.group,
				# 		"group_name": data.group,
				# 		"is_active": 1		
				# 	})
					
				# 	item = frappe.get_doc("Item", data.parent_item)
				# 	mi.append("data_group", {
				# 		"doctype": "Data Group",
				# 		"item_code_variant" : data.item_code_variant,
				# 		"colour" : data.colour,
				# 		"yard_atau_meter_per_roll" : data.yard_atau_meter_per_roll,
				# 		"parent_item" : data.parent_item,
				# 		"item_name" : data.item_name,
				# 		"warehouse" : data.warehouse
				# 	})

				# 	mi.flags.ignore_permissions = 1
				# 	mi.save()


	# packing list data pcs
	# if doc.packing_list_data_pcs :
	# 	temp_gruop = []
	# 	g = ""
	# 	c = 0
	# 	panjang = len(doc.packing_list_data_pcs)
	# 	for data in doc.packing_list_data_pcs :
	# 		if data.group_pcs == g :
	# 			g = data.group_pcs
	# 			c = c + 1
				
	# 		else :
	# 			temp_gruop.append(data.group_pcs)
	# 			g = data.group_pcs
	# 			c = c + 1
	# 			if panjang == c :
	# 				temp_gruop.append(data.group_pcs)

	# 	for t in temp_gruop :
	# 		meow = 0
	# 		cek_group = frappe.db.sql("""
	# 			SELECT
	# 			mi.`group_code`
	# 			FROM `tabGroup Item` mi
	# 			WHERE mi.`group_code` = "{}"
	# 			""".format(t[0]))

	# 		if cek_group :
	# 			meow = 0
	# 		else :
	# 			mi = frappe.new_doc("Group Item")
	# 			mi.update({
	# 				"group_code": t[0],
	# 				"group_name": t[0],
	# 				"uom" : t[1],
	# 				"is_active": 1		
	# 			})
	# 			mi.flags.ignore_permissions = 1
	# 			mi.save()

	# 	count = 0
	# 	for data in doc.packing_list_data_pcs :
	# 		if data.group_pcs :
	# 			cek_group = frappe.db.sql("""
	# 				SELECT
	# 				mi.`group_code`
	# 				FROM `tabGroup Item` mi
	# 				WHERE mi.`group_code` = "{}"
	# 				AND mi.`uom` = "{}"
	# 				""".format(data.group_pcs, data.uom_pcs))

	# 			if cek_group :
	# 				cek_data = frappe.db.sql("""
	# 					SELECT 
	# 					di.`item_code_pcs`
	# 					FROM `tabData Group` di
	# 					WHERE di.`item_code_pcs` = "{}"
	# 				""".format(data.item_code_pcs))

	# 				if cek_data :
	# 					count = 0
	# 				else :
						
	# 					mi = frappe.get_doc("Group Item", data.group_pcs)
	# 					mi.append("data_group", {
	# 					"doctype": "Data Group",
	# 					"item_code_pcs" : data.item_code_pcs,
	# 					"item_name_pcs" : data.item_name_pcs,
	# 					"parent_item_pcs" : data.parent_item_pcs,
	# 					"warehouse_pcs" : data.warehouse_pcs,
	# 					"uom_pcs" : "PCS"
	# 				})
	# 				mi.flags.ignore_permissions = 1
	# 				mi.save()

				# else :
				# 	mi = frappe.new_doc("Group Item")
				# 	mi.update({
				# 		"group_code": data.group_pcs,
				# 		"group_name": data.group_pcs,
				# 		"is_active": 1		
				# 	})
					
				# 	item = frappe.get_doc("Item", data.parent_item_pcs)
				# 	mi.append("data_group", {
				# 		"doctype": "Data Group",
				# 		"item_code_pcs" : data.item_code_pcs,
				# 		"item_name_pcs" : data.item_name_pcs,
				# 		"parent_item_pcs" : data.parent_item_pcs,
				# 		"warehouse_pcs" : data.warehouse_pcs
				# 	})

				# 	mi.flags.ignore_permissions = 1
				# 	mi.save()


@frappe.whitelist()
def cancel_packing_list_receipt(doc,method):
	# pass
	count = 0
	temp_group = ""
	if doc.packing_list_data :
		for data in doc.packing_list_data :
			if data.group :
				if temp_group == data.group :
					temp_group = data.group
				else :
					temp_group = data.group
					cek_group = frappe.get_doc("Group Item",temp_group).is_used
					if cek_group == 1 :
						frappe.throw("Tidak dapat di hapus karena Group sudah di alokasikan")
					else :
						mi = frappe.get_doc("Group Item", temp_group)
						mi.flags.ignore_permissions = 1
						mi.cancel()
						frappe.db.sql ("""
							DELETE FROM `tabGroup Item`
							WHERE name = "{0}"
							""".format(temp_group))

					# frappe.db.commit()



@frappe.whitelist()
def create_purchase_receipt(doc,method):

	if doc.is_return : 
		cek_data = frappe.db.sql("""
			SELECT prec.`name` FROM `tabPurchase Receipt` prec
			WHERE prec.`packing_list_receipt` = "{}"
			AND prec.`docstatus` = 1
		""".format(doc.return_against))


		pr_doc = frappe.new_doc("Purchase Receipt")
		pr_doc.update({
			"supplier": doc.supplier,
			"supplier_name" : doc.supplier_name,
			"posting_date" : doc.posting_date,
			"posting_time" : doc.posting_time,
			"packing_list_receipt" : doc.name,
			"is_return" : 1,
			"return_against" : cek_data[0][0],
			"currency" : po.currency,
			"buying_price_list" : po.buying_price_list,
			"conversion_rate" : po.conversion_rate

		})
	else :
		po = frappe.get_doc("Purchase Order", doc.purchase_order)
		pr_doc = frappe.new_doc("Purchase Receipt")
		pr_doc.update({
			"supplier": doc.supplier,
			"supplier_name" : doc.supplier_name,
			"posting_date" : doc.posting_date,
			"posting_time" : doc.posting_time,
			"packing_list_receipt" : doc.name,
			"currency" : po.currency,
			"buying_price_list" : po.buying_price_list,
			"conversion_rate" : po.conversion_rate
		})


	item_code = ""
	item_name = ""
	description = ""
	received_qty = 0
	qty = 0
	uom = ""
	stock_uom = ""
	rate = 0
	amount = 0
	warehouse = ""
	purchase_order = ""
	schedule_date = ""
	stock_qty = 0
	purchase_order_item = ""

	count = 0
	length_arr = len(doc.packing_list_data)

	for i in doc.packing_list_data :
		if item_code == i.item_code_variant :
			
			received_qty = received_qty + i.total_yard_atau_meter
			qty = qty + i.total_yard_atau_meter
			amount = amount
			stock_qty = stock_qty + i.total_yard_atau_meter
			
			count = count + 1

			if count == length_arr :
				pr_doc.append("items", {
					"item_code" :item_code,
					"item_name" :item_name,
					"description" :description,
					"received_qty" :received_qty,
					"qty" :qty,
					"uom" :uom,
					"stock_uom" :stock_uom,
					"rate" :rate,
					"amount" :amount,
					"warehouse" :warehouse,
					"purchase_order" :purchase_order,
					"stock_qty": stock_qty,
					"purchase_order_item" : purchase_order_item
				})

		else :
			if count == 0 :
				get_poi = frappe.db.sql("""
					SELECT
					poi.`name`,
					poi.`item_code`,
					poi.`schedule_date`
					FROM `tabPurchase Order Item` poi
					WHERE poi.`parent` = "{}"
					AND poi.`item_code` = "{}"
				""".format(doc.purchase_order, i.item_code_variant))
				
				item_code = i.item_code_variant
				item_name = i.item_name
				description = i.item_name
				received_qty = i.total_yard_atau_meter
				qty = i.total_yard_atau_meter
				uom = i.inventory_uom
				stock_uom = i.inventory_uom
				rate = 0
				amount = 0
				warehouse = i.warehouse
				purchase_order = doc.purchase_order
				schedule_date = get_poi[0][2]
				stock_qty = i.total_yard_atau_meter
				purchase_order_item = get_poi[0][0]

				count = count + 1


				if count == length_arr :
					pr_doc.append("items", {
						"item_code" :item_code,
						"item_name" :item_name,
						"description" :description,
						"received_qty" :received_qty,
						"qty" :qty,
						"uom" :uom,
						"stock_uom" :stock_uom,
						"rate" :rate,
						"amount" :amount,
						"warehouse" :warehouse,
						"purchase_order" :purchase_order,
						"stock_qty": stock_qty,
						"purchase_order_item" : purchase_order_item
					})
					

			else :
				pr_doc.append("items", {
					"item_code" :item_code,
					"item_name" :item_name,
					"description" :description,
					"received_qty" :received_qty,
					"qty" :qty,
					"uom" :uom,
					"stock_uom" :stock_uom,
					"rate" :rate,
					"amount" :amount,
					"warehouse" :warehouse,
					"purchase_order" :purchase_order,
					"stock_qty": stock_qty,
					"purchase_order_item" : purchase_order_item
				})
				

				get_poi = frappe.db.sql("""
					SELECT
					poi.`name`,
					poi.`item_code`,
					poi.`schedule_date`
					FROM `tabPurchase Order Item` poi
					WHERE poi.`parent` = "{}"
					AND poi.`item_code` = "{}"
				""".format(doc.purchase_order, i.item_code_variant))
				
				item_code = i.item_code_variant
				item_name = i.item_name
				description = i.item_name
				received_qty = i.total_yard_atau_meter
				qty = i.total_yard_atau_meter
				uom = i.inventory_uom
				stock_uom = i.inventory_uom
				rate = 0
				amount = 0
				warehouse = i.warehouse
				purchase_order = doc.purchase_order
				schedule_date = get_poi[0][2]
				stock_qty = i.total_yard_atau_meter
				purchase_order_item = get_poi[0][0]

				count = count + 1

				if count == length_arr :
					pr_doc.append("items", {
						"item_code" :item_code,
						"item_name" :item_name,
						"description" :description,
						"received_qty" :received_qty,
						"qty" :qty,
						"uom" :uom,
						"stock_uom" :stock_uom,
						"rate" :rate,
						"amount" :amount,
						"warehouse" :warehouse,
						"purchase_order" :purchase_order,
						"stock_qty": stock_qty,
						"purchase_order_item" : purchase_order_item
					})

	if doc.packing_list_data_pcs :
		for i in doc.packing_list_data_pcs :
			get_poi = frappe.db.sql("""
				SELECT
				poi.`name`,
				poi.`item_code`,
				poi.`schedule_date`
				FROM `tabPurchase Order Item` poi
				WHERE poi.`parent` = "{}"
				AND poi.`item_code` = "{}"
			""".format(doc.purchase_order, i.item_code_pcs))

			if get_poi :

				pr_doc.append("items", {
					"item_code" :i.item_code_pcs,
					"item_name" :i.item_name_pcs,
					"description" :i.item_name_pcs,
					"received_qty" :i.total_pcs,
					"qty" :i.total_pcs,
					"uom" :i.uom_pcs,
					"stock_uom" :i.total_pcs,
					"rate" :0,
					"amount" :0,
					"warehouse" :i.warehouse_pcs,
					"purchase_order" : doc.purchase_order,
					"schedule_date" : get_poi[0][2],
					"stock_qty": i.total_pcs,
					"purchase_order_item" : get_poi[0][0]
				})
			else :
				pr_doc.append("items", {
					"item_code" :i.item_code_pcs,
					"item_name" :i.item_name_pcs,
					"description" :i.item_name_pcs,
					"received_qty" :i.total_pcs,
					"qty" :i.total_pcs,
					"uom" :i.uom_pcs,
					"stock_uom" :i.total_pcs,
					"rate" :0,
					"amount" :0,
					"warehouse" :i.warehouse_pcs,
					"stock_qty": i.total_pcs
				})
					


	pr_doc.flags.ignore_permissions = 1
	pr_doc.submit()


@frappe.whitelist()
def cancel_purchase_receipt(doc,method):
	get_prec = frappe.db.sql("""
		SELECT
		pr.`name`,
		pr.`packing_list_receipt`
		FROM `tabPurchase Receipt` pr
		WHERE pr.`packing_list_receipt` = "{}"
	""".format(doc.name))

	pr_doc = frappe.get_doc("Purchase Receipt", get_prec[0][0])
	pr_doc.flags.ignore_permissions = 1
	pr_doc.cancel()




@frappe.whitelist()
def save_packing_list_receipt(doc,method):

	if doc.packing_list_data :
		for i in doc.packing_list_data :
			item = frappe.get_doc("Item", i.item_code_variant)
			i.item_name = item.item_name
			i.inventory_uom = item.stock_uom
			i.warehouse = item.default_warehouse
			i.total_yard_atau_meter = float(i.total_roll) * float(i.yard_atau_meter_per_roll)
			


	if doc.packing_list_data_pcs :
		for i in doc.packing_list_data_pcs :
			item = frappe.get_doc("Item", i.item_code_pcs)
			i.item_name_pcs = item.item_name
			i.pcs_uom = item.stock_uom
			i.warehouse = item.default_warehouse
			


	if doc.is_return :
		prev_doc = doc.return_against

		arr_total_roll = frappe.db.sql("""
			SELECT
			SUM(plrd.`total_yard_atau_meter`)
			FROM `tabPacking List Receipt Data` plrd
			WHERE plrd.`parent` = "{}"
			GROUP BY plrd.`parent`
		""".format(prev_doc))

		arr_total_pcs = frappe.db.sql("""
			SELECT
			SUM(plrc.`total_pcs`)
			FROM `tabPacking List Receipt PCS` plrc
			WHERE plrc.`parent` = "{}"
			GROUP BY plrc.`parent`
		""".format(prev_doc))

		total_yard = 0
		if doc.packing_list_data :
			for i in doc.packing_list_data :
				total_yard = total_yard + i.total_yard_atau_meter

			if total_yard > arr_total_roll[0] :
				frappe.throw("Tidak dapat di save karena jumlah Yard/Meter retur lebih besar")


		total_pcs = 0
		if doc.packing_list_data_pcs :
			for i in doc.packing_list_data_pcs :
				total_pcs = total_pcs + i.total_pcs

			if total_pcs > arr_total_pcs[0] :
				frappe.throw("Tidak dapat di save karena jumlah Pcs retur lebih besar")




@frappe.whitelist()
def get_data_from_purchase_order(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.posting_date = source.transaction_date
		target.supplier = source.supplier
		target.supplier_name = source.supplier_name
		target.purchase_order = source.name
		target.supplier_invoice_no = source.supplier_invoice_no
		target.invoice_date = source.invoice_date

	def update_item(source_doc, target_doc, source_parent):
		target_doc.item_code = source_doc.item_code
		target_doc.qty_yard = source_doc.qty
		target_doc.qty_roll = source_doc.roll_qty
		target_doc.uom = source_doc.stock_uom

	target_doc = get_mapped_doc("Purchase Order", source_name, {
		"Purchase Order": {
			"doctype": "Packing List Receipt",
			"validation": {
				"docstatus": ["=", 1]
			},
		},
		"Purchase Order Item": {
			"doctype": "Summary Purchase Order",
			"postprocess": update_item
		}
		
	}, target_doc, set_missing_values)

	return target_doc






@frappe.whitelist()
def submit_purchase_receipt(doc,method):
	pass
	# if doc.packing_list_receipt and doc.purchase_order:
	# 	frappe.db.sql ("""
	# 		update 
	# 		`tabPacking List Receipt` 
	# 		set 
	# 		is_used=1
	# 		where 
	# 		name="{0}"
	# 		 """.format(doc.packing_list_receipt))

	# 	# frappe.db.commit()
		# msgprint("Akan mengganti data di PO yang bersangkutan sesuai dengan Packing List Receipt (masih on progress)")

@frappe.whitelist()
def cancel_purchase_receipt(doc,method):
	pass
	# if doc.packing_list_receipt and doc.purchase_order:
	# 	frappe.db.sql ("""
	# 		update 
	# 		`tabPacking List Receipt` 
	# 		set 
	# 		is_used=0
	# 		where 
	# 		name="{0}"
	# 		 """.format(doc.packing_list_receipt))

	# 	# frappe.db.commit()
		# msgprint("Akan mengembalikan data PO seperti semua (masih on progress)")



@frappe.whitelist()
def make_packing_list_receipt_return(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.is_return = 1
		target.return_against = source.name

	def update_item_roll(source_doc, target_doc, source_parent):
		target_doc.total_roll = -1* source_doc.total_roll
		target_doc.total_yard_atau_meter = -1* source_doc.total_yard_atau_meter

	def update_item_pcs(source_doc, target_doc, source_parent):
		target_doc.total_pcs = -1* source_doc.total_pcs
		

	target_doc = get_mapped_doc("Packing List Receipt", source_name, {
		"Packing List Receipt": {
			"doctype": "Packing List Receipt",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		# "Packing List Receipt Data": {
		# 	"doctype": "Packing List Receipt Data",
		# 	"postprocess": update_item_roll
		# },
		# "Packing List Receipt PCS": {
		# 	"doctype": "Packing List Receipt PCS",
		# 	"postprocess": update_item_pcs
		# }
		
	}, target_doc, set_missing_values)

	return target_doc

@frappe.whitelist()
def change_status_document(name,status_document,tab):
	frappe.db.sql(""" UPDATE `{0}`i SET i.`status_document`="{1}" WHERE i.`name`="{2}"  """.format(tab,status_document,name))
	frappe.db.commit();
	return ""