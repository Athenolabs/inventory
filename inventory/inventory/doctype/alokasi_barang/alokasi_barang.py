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
	"alokasi_barang_data": "templates/includes/alokasi_barang.html",
	"summary_pending_order_roll": "templates/includes/summary_pending_order.html",
	"pending_order_group_temp": "templates/includes/pending_order_group_temp.html"
}


class AlokasiBarang(Document):

	# def generat_item(self):
	# 	if self.item_code_upload and self.warehouse_upload and self.alokasi_barang_temp :
	# 		sorted_table = sorted(self.alokasi_barang_temp, key=operator.itemgetter(0, 1, 2))

	# 		item_code = self.item_code_upload
	# 		warehouse = self.warehouse_upload
	# 		uom = ""
	# 		group = ""
	# 		colour = ""
	# 		per_roll = ""
	# 		total_roll = 0
	# 		total_yard_atau_meter = 0
			
	# 		for i in sorted_table :


	# 	else :
	# 		frappe.throw("Item Code / Warehouse / Tabel tidak ada isinya")

	def get_data_group(self):
		count = 0
		if self.pending_order_group_temp :
			for dg in self.pending_order_group_temp :
				item = frappe.get_doc("Item", dg.item_code_variant)
				
				pp_so = self.append('alokasi_barang_data', {})
				pp_so.item_code_roll = dg.item_code_variant
				pp_so.item_name_roll = item.item_name
				pp_so.colour = dg.colour
				pp_so.roll_qty = dg.total_roll
				pp_so.group = dg.group_code
				pp_so.inventory_uom = item.stock_uom
				pp_so.yard_atau_meter_per_roll = dg.yard_atau_meter_per_roll
				
				pp_so.qty_dialokasi = 0
				pp_so.qty_terkirim = 0
				pp_so.rate = dg.rate
				pp_so.total_rate = dg.rate * dg.total_roll
				pp_so.warehouse = item.default_warehouse

			self.pending_order_group_temp = []

		else :
			frappe.throw("Data Group tidak ada")

	def get_group(self):
		if self.group_item :
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
				ORDER BY dg.`idx`

			""".format(self.group_item))


			if get_data_group :
				for dg in get_data_group :
						
					pp_so = self.append('pending_order_group_temp', {})
					pp_so.item_code_variant = dg[2]
					pp_so.colour = dg[5]
					pp_so.total_roll = dg[9]
					pp_so.yard_atau_meter_per_roll = dg[6]
					pp_so.group_code = dg[0]

					qty_pending_order = 0
					qty_terkirim = 0
					qty_dialokasi = 0
					qty_inventory = 0

					get_qty_inventory = frappe.db.sql("""
						SELECT
						SUM(di.`total_roll`)
						FROM `tabData Inventory` di
						WHERE di.`item_code_variant` = "{}"
						AND di.`colour` = "{}"
						AND di.`group` = "{}"

						GROUP BY di.`item_code_variant`
						""".format(dg[2], dg[5], self.group_item))

					get_qty_pending_order = frappe.db.sql("""
						SELECT
						SUM(por.`roll_qty`)

						FROM `tabPending Order` po
						JOIN `tabPending Order Roll` por
						ON po.`name` = por.`parent`
						WHERE po.`docstatus` < 2
						AND por.`docstatus` < 2
						AND por.`item_code_roll` = "{}"
						AND por.`colour` = "{}"
						GROUP BY por.`item_code_roll`
						""".format(dg[2], dg[5]))

					get_qty_dialokasi = frappe.db.sql("""
						SELECT
						SUM(por.`roll_qty`)

						FROM `tabAlokasi Barang` po
						JOIN `tabAlokasi Barang Data` por
						ON po.`name` = por.`parent`
						WHERE po.`docstatus` < 2
						AND por.`docstatus` < 2
						AND por.`item_code_roll` = "{}"
						AND por.`colour` = "{}"
						AND por.`group` = "{}"
						GROUP BY por.`item_code_roll`
						""".format(dg[2], dg[5], self.group_item))

					get_qty_terkirim = frappe.db.sql("""
						SELECT
						SUM(por.`roll_qty`)

						FROM `tabPacking List Delivery` po
						JOIN `tabPacking List Delivery Data` por
						ON po.`name` = por.`parent`
						WHERE po.`docstatus` < 2
						AND por.`docstatus` < 2
						AND por.`item_code_roll` = "{}"
						AND por.`colour` = "{}"
						AND por.`group` = "{}"
						GROUP BY por.`item_code_roll`
						""".format(dg[2], dg[5], self.group_item))

					if get_qty_pending_order :
						qty_pending_order = float(get_qty_pending_order[0][0])
					else :
						qty_pending_order = 0
					if get_qty_terkirim :
						qty_terkirim = float(get_qty_terkirim[0][0])
					else :
						qty_terkirim = 0
					if get_qty_dialokasi :
						qty_dialokasi = float(get_qty_dialokasi[0][0])
					else :
						qty_dialokasi = 0
					if get_qty_inventory :
						qty_inventory = float(get_qty_inventory[0][0])
					else :
						qty_inventory = 0


					if qty_pending_order == 0 :
						pp_so.qty_pending_order = 0
					else :
						pp_so.qty_pending_order = qty_pending_order 

					if qty_dialokasi == 0 :
						pp_so.qty_alokasi_barang = 0
					else :
						pp_so.qty_alokasi_barang = qty_dialokasi

					if qty_terkirim == 0 :
						pp_so.qty_terkirim = 0
					else :
						pp_so.qty_terkirim = qty_terkirim

					if qty_inventory == 0 :
						pp_so.qty_inventory = 0
					else :
						pp_so.qty_inventory = qty_inventory - pp_so.qty_alokasi_barang
						
			else :
				frappe.throw("Group Tidak Active / Tidak Memiliki Item")

		else :
			frappe.throw("Group Item belum dipilih")


	def add_pcs(self):
		if self.item_code_pcs and self.qty_pcs and self.warehouse_pcs :
			if self.uom_pcs == "Pcs" :
				if self.alokasi_barang_pcs :
					if self.qty_pcs > self.jumlah_di_stock :
						msgprint("Qty yang akan di inputkan lebih besar daripada yang ada di Inventory")

					for i in self.alokasi_barang_pcs :
						if i.item_code_pcs == self.item_code_pcs and i.warehouse == self.warehouse_pcs and i.rate == self.rate_pcs :
							count = 1

					if count == 1 :
						for i in self.alokasi_barang_pcs :
							if i.item_code_pcs == self.item_code_pcs and i.warehouse == self.warehouse_pcs and i.rate == self.rate_pcs :
								new_total_roll = i.pcs_qty
								i.pcs_qty = new_total_roll + self.qty_pcs

								new_total_rate = i.total_rate
								i.total_rate = new_total_rate + (self.qty_pcs * self.rate_pcs)
					else :
						pp_so = self.append('alokasi_barang_pcs', {})
						pp_so.item_code_pcs = self.item_code_pcs
						pp_so.item_name_roll = self.item_name_pcs
						pp_so.pcs_qty = self.qty_pcs

						pp_so.pcs_uom = frappe.get_doc("Item",self.item_code_pcs).stock_uom
						
						pp_so.qty_dialokasi = 0
						pp_so.qty_terkirim = 0
						pp_so.rate = self.rate_pcs
						pp_so.total_rate = self.rate_pcs * self.qty_pcs
						pp_so.warehouse = self.warehouse_pcs
				else :
					pp_so = self.append('alokasi_barang_pcs', {})
					pp_so.item_code_pcs = self.item_code_pcs
					pp_so.item_name_roll = self.item_name_pcs
					pp_so.pcs_qty = self.qty_pcs

					pp_so.pcs_uom = frappe.get_doc("Item",self.item_code_pcs).stock_uom
					
					pp_so.qty_dialokasi = 0
					pp_so.qty_terkirim = 0
					pp_so.rate = self.rate_pcs
					pp_so.total_rate = self.rate_pcs * self.qty_pcs
					pp_so.warehouse = self.warehouse_pcs

			
			self.qty_pcs = 0
			self.rate_pcs = 0
			

			self.jumlah_di_stock = 0
			self.jumlah_alokasi_barang_pcs = 0
			self.jumlah_di_pending_order_pcs = 0


		else :
			frappe.throw("Item Code / Qty / Warehouse tidak ada isinya")



	def add_item(self):
		count = 0
		if self.item_code and self.qty and self.warehouse :
			if self.uom == "Yard" or self.uom == "Meter" :
				if self.colour_pending_order :
					if self.qty > self.jumlah_di_inventory :
						frappe.throw("Qty yang akan di inputkan lebih besar daripada yang ada di Inventory")
					if self.alokasi_barang_data :
						for i in self.alokasi_barang_data :
							if i.item_code_roll == self.item_code and i.colour == self.colour_pending_order and i.warehouse == self.warehouse and i.rate == self.rate :
								count = 1

						if count == 1 :
							for i in self.alokasi_barang_data :
								if i.item_code_roll == self.item_code and i.colour == self.colour_pending_order and i.warehouse == self.warehouse and i.rate == self.rate :
									new_total_roll = i.roll_qty
									i.roll_qty = new_total_roll + self.qty

									new_total_yard_atau_meter = i.total_yard_atau_meter
									i.total_yard_atau_meter = new_total_yard_atau_meter + (self.qty * self.yard_atau_meter_per_roll)

									new_total_rate = i.total_rate
									i.total_rate = new_total_rate + (self.qty * self.rate)

						else :
							pp_so = self.append('alokasi_barang_data', {})
							pp_so.item_code_roll = self.item_code
							pp_so.item_name_roll = self.item_name
							pp_so.colour = self.colour_pending_order
							pp_so.roll_qty = self.qty
							pp_so.inventory_uom = frappe.get_doc("Item",self.item_code).stock_uom

							pp_so.total_yard_atau_meter = (self.qty * self.yard_atau_meter_per_roll)
							pp_so.yard_atau_meter_per_roll = self.yard_atau_meter_per_roll
							
							pp_so.qty_dialokasi = 0
							pp_so.qty_terkirim = 0
							pp_so.rate = self.rate
							pp_so.total_rate = self.rate * self.qty
							pp_so.warehouse = self.warehouse
					
					else :
						pp_so = self.append('alokasi_barang_data', {})
						pp_so.item_code_roll = self.item_code
						pp_so.item_name_roll = self.item_name
						pp_so.colour = self.colour_pending_order
						pp_so.roll_qty = self.qty

						pp_so.inventory_uom = frappe.get_doc("Item",self.item_code).stock_uom

						pp_so.total_yard_atau_meter = (self.qty * self.yard_atau_meter_per_roll)
						pp_so.yard_atau_meter_per_roll = self.yard_atau_meter_per_roll
						
						pp_so.qty_dialokasi = 0
						pp_so.qty_terkirim = 0
						pp_so.rate = self.rate
						pp_so.total_rate = self.rate * self.qty
						pp_so.warehouse = self.warehouse


					
					self.colour_pending_order = ""
					self.yard_atau_meter_per_roll = 0
					self.qty = 0
					self.rate = 0
					

					self.jumlah_di_inventory = 0
					self.jumlah_alokasi_barang = 0
					self.jumlah_di_pending_order = 0

				else :
					frappe.throw("Colour tidak ada isinya")

			# elif self.uom == "Pcs" :
			# 	if self.alokasi_barang_pcs :
			# 		if self.qty > self.jumlah_di_inventory :
			# 			msgprint("Qty yang akan di inputkan lebih besar daripada yang ada di Inventory")

			# 		for i in self.alokasi_barang_pcs :
			# 			if i.item_code_pcs == self.item_code and i.warehouse == self.warehouse and i.rate == self.rate :
			# 				count = 1

			# 		if count == 1 :
			# 			for i in self.alokasi_barang_pcs :
			# 				if i.item_code_pcs == self.item_code and i.warehouse == self.warehouse and i.rate == self.rate :
			# 					new_total_roll = i.pcs_qty
			# 					i.pcs_qty = new_total_roll + self.qty

			# 					new_total_rate = i.total_rate
			# 					i.total_rate = new_total_rate + (self.qty * self.rate)
			# 		else :
			# 			pp_so = self.append('alokasi_barang_pcs', {})
			# 			pp_so.item_code_pcs = self.item_code
			# 			pp_so.item_name_roll = self.item_name
			# 			pp_so.pcs_qty = self.qty

			# 			pp_so.pcs_uom = frappe.get_doc("Item",self.item_code).stock_uom
						
			# 			pp_so.qty_dialokasi = 0
			# 			pp_so.qty_terkirim = 0
			# 			pp_so.rate = self.rate
			# 			pp_so.total_rate = self.rate * self.qty
			# 			pp_so.warehouse = self.warehouse
			# 	else :
			# 		pp_so = self.append('alokasi_barang_pcs', {})
			# 		pp_so.item_code_pcs = self.item_code
			# 		pp_so.item_name_roll = self.item_name
			# 		pp_so.pcs_qty = self.qty

			# 		pp_so.pcs_uom = frappe.get_doc("Item",self.item_code).stock_uom
					
			# 		pp_so.qty_dialokasi = 0
			# 		pp_so.qty_terkirim = 0
			# 		pp_so.rate = self.rate
			# 		pp_so.total_rate = self.rate * self.qty
			# 		pp_so.warehouse = self.warehouse

			
			self.qty = 0
			self.rate = 0
			

			self.jumlah_di_inventory = 0
			self.jumlah_alokasi_barang = 0
			self.jumlah_di_pending_order = 0

		else :
			frappe.throw("Item Code / Qty / Warehouse tidak ada isinya")


@frappe.whitelist()
def save_alokasi_barang(doc,method):

	# cek item alokasi dan pending order sama atau tidak
	if doc.alokasi_barang_data :
		for d in doc.alokasi_barang_data :
			item_code = d.item_code_roll
			colour = d.colour
			uom = d.inventory_uom
			qty = d.roll_qty

			count = 0
			count_qty = 0
			for i in doc.summary_pending_order_roll :
				item = frappe.get_doc("Item",i.item_code_roll)
				if i.item_code_roll == item_code and item.stock_uom == uom and i.colour == colour :
					count = 1

			if count == 0 :
				msgprint("Item ("+item_code+" = "+colour+") tidak ada di dalam Pending Order")


	# perhitungan komisi di alokasi
	commission_percentage = 0
	commission_rate = 0
	if doc.sales_type == "%" :
		if doc.commission_percentage :
			commission_percentage = doc.commission_percentage
	else :
		if doc.commission_rate :
			commission_rate = doc.commission_rate


	total_rate = 0
	total_commission = 0
	outstanding_amount = 0

	if doc.alokasi_barang_data :
		for i in doc.alokasi_barang_data :
			i.total_rate = i.roll_qty * i.rate
			total_rate = total_rate + i.total_rate
			i.qty_sisa = i.roll_qty
			i.total_yard_atau_meter = i.roll_qty * i.yard_atau_meter_per_roll
			

	if doc.alokasi_barang_pcs :
		for i in doc.alokasi_barang_pcs :
			i.total_rate = i.pcs_qty * i.rate
			total_rate = total_rate + i.total_rate
			i.qty_sisa = i.pcs_qty
			

	doc.grand_total = total_rate
	doc.outstanding_amount = total_rate
	if doc.sales_type == "%" :
		doc.total_commission = total_rate * doc.commission_percentage / 100
	else :
		doc.total_commission = doc.commission_rate

	# if doc.alokasi_barang_data :
	# 	for i in doc.alokasi_barang_data :
	# 		item = frappe.get_doc("Item", i.item_code_roll)
	# 		i.item_name_roll = item.item_name
	# 		i.inventory_uom = item.stock_uom
	# 		i.warehouse = item.default_warehouse
	# 		i.total_yard_atau_meter = float(i.roll_qty) * float(i.yard_atau_meter_per_roll)
	# 		if i.rate :
	# 			i.total_rate = float(i.rate) * float(i.yard_atau_meter_per_roll)


	# if doc.alokasi_barang_pcs :
	# 	for i in doc.alokasi_barang_data :
	# 		item = frappe.get_doc("Item", i.item_code_pcs)
	# 		i.item_name_pcs = item.item_name
	# 		i.pcs_uom = item.stock_uom
	# 		i.warehouse = item.default_warehouse
	# 		if i.rate :
	# 			i.total_rate = float(i.rate) * float(i.pcs_qty)


	# commission_percentage = 0
	# commission_rate = 0
	# if doc.sales_type == "%" :
	# 	if doc.commission_percentage :
	# 		commission_percentage = doc.commission_percentage
	# else :
	# 	if doc.commission_rate :
	# 		commission_rate = doc.commission_rate


	# total_rate = 0
	# total_commission = 0
	# outstanding_amount = 0

	# if doc.alokasi_barang_data :
	# 	for i in doc.alokasi_barang_data :
	# 		total_rate = total_rate + i.total_rate
	# 		i.qty_sisa = i.roll_qty

	# if doc.alokasi_barang_pcs :
	# 	for i in doc.alokasi_barang_pcs :
	# 		total_rate = total_rate + i.total_rate
	# 		i.qty_sisa = i.pcs_qty

	# doc.grand_total = total_rate
	# doc.outstanding_amount = total_rate
	# if doc.sales_type == "%" :
	# 	doc.total_commission = total_rate * doc.commission_percentage / 100
	# else :
	# 	doc.total_commission = total_rate + doc.commission_rate





@frappe.whitelist()
def submit_alokasi_barang(doc,method):

	# cek item alokasi dan pending order sama atau tidak
	if doc.alokasi_barang_data :
		for d in doc.alokasi_barang_data :
			item_code = d.item_code_roll
			colour = d.colour
			uom = d.inventory_uom
			qty = d.roll_qty

			count = 0
			count_qty = 0
			for i in doc.summary_pending_order_roll :
				item = frappe.get_doc("Item",i.item_code_roll)
				if i.item_code_roll == item_code and item.stock_uom == uom and i.colour == colour :
					count = 1

			if count == 0 :
				frappe.throw("Item ("+item_code+" = "+colour+") tidak ada di dalam Pending Order")


	# create new item jika tidak ada di dalam master inventory
	for i in doc.alokasi_barang_data :
		item_code = d.item_code_roll
		colour = d.colour
		uom = d.inventory_uom
		qty = d.roll_qty
		yard_atau_meter_per_roll = d.yard_atau_meter_per_roll
		item = frappe.get_doc("Item",item_code)

		count = 0

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
		""".format(item_code, yard_atau_meter_per_roll, item.default_warehouse, colour, uom))

		if cek_data :
			count = 1
		else :
			mi = frappe.get_doc("Master Inventory", item_code)
			mi.append("data_inventory", {
				"doctype": "Data Inventory",
				"item_code_variant" : item_code,
				"yard_atau_meter_per_roll" : yard_atau_meter_per_roll,
				"total_roll" : 0,
				"total_yard_atau_meter" : 0,
				"warehouse" : item.default_warehouse,
				"colour" : colour,
				"inventory_uom" : uom
			})

			mi.flags.ignore_permissions = 1
			mi.save()



	# update group item to use
	count = 0
	temp_group = ""
	if doc.alokasi_barang_data :
		for data in doc.alokasi_barang_data :
			if data.group :
				if temp_group == data.group :
					temp_group = data.group
				else :
					temp_group = data.group
					frappe.db.sql ("""
						update 
						`tabGroup Item` 
						set 
						is_used=1
						where 
						name="{0}"
				
						""".format(temp_group))
	# if doc.pending_order :
	# 	if doc.alokasi_barang_data : 
	# 		for i in doc.alokasi_barang_data :
	# 			get_data_pending_order = frappe.db.sql("""
	# 				SELECT
	# 				por.`roll_qty`,
	# 				por.`qty_sisa`,
	# 				por.`qty_terkirim`,
	# 				por.`qty_dialokasi`
	# 				FROM `tabPending Order Roll` por
	# 				WHERE por.`parent`= "{}"
	# 				AND por.`item_code_roll` = "{}"
	# 				AND por.`colour` = "{}"

	# 			""".format(doc.pending_order, i.item_code_roll, i.colour))
	# 			if get_data_pending_order[0][3] :
	# 				temp_qty_dialokasi = get_data_pending_order[0][3]
	# 			else :
	# 				temp_qty_dialokasi = 0

	# 			new_qty_dialokasi = temp_qty_dialokasi + i.roll_qty

	# 			frappe.db.sql ("""
	# 				update 
	# 				`tabPending Order Roll` 
	# 				set 
	# 				qty_dialokasi="{0}"
	# 				where 
	# 				item_code_roll="{1}"
	# 				and 
	# 				colour = "{2}"
					
	# 				""".format(new_qty_dialokasi, i.item_code_roll, i.colour))
					

	# 	if doc.alokasi_barang_pcs :
	# 		for i in doc.alokasi_barang_data :
	# 			get_data_pending_order = frappe.db.sql("""
	# 				SELECT
	# 				por.`pcs_qty`,
	# 				por.`qty_sisa`,
	# 				por.`qty_terkirim`,
	# 				por.`qty_dialokasi`
	# 				FROM `tabPending Order Pcs` por
	# 				WHERE por.`parent`= "{}"
	# 				AND por.`item_code_pcs` = "{}"

	# 			""".format(doc.pending_order, i.item_code_pcs))
	# 			if get_data_pending_order[0][3] :
	# 				temp_qty_dialokasi = get_data_pending_order[0][3]
	# 			else :
	# 				temp_qty_dialokasi = 0

	# 			new_qty_dialokasi = temp_qty_dialokasi + i.pcs_qty

	# 			frappe.db.sql ("""
	# 				update 
	# 				`tabPending Order Pcs` 
	# 				set 
	# 				qty_dialokasi="{0}"
	# 				where 
	# 				item_code_pcs="{1}"
					
	# 				""".format(new_qty_dialokasi, i.item_code_pcs))



@frappe.whitelist()
def cancel_alokasi_barang(doc,method):
	count = 0
	temp_group = ""
	for data in doc.alokasi_barang_data :
		if data.group :
			if temp_group == data.group :
				temp_group = data.group
			else :
				temp_group = data.group
				frappe.db.sql ("""
					update 
					`tabGroup Item` 
					set 
					is_used=0
					where 
					name="{0}"
			
					""".format(temp_group))
	# if doc.pending_order :
	# 	if doc.alokasi_barang_data : 
	# 		for i in doc.alokasi_barang_data :
	# 			get_data_pending_order = frappe.db.sql("""
	# 				SELECT
	# 				por.`roll_qty`,
	# 				por.`qty_sisa`,
	# 				por.`qty_terkirim`,
	# 				por.`qty_dialokasi`
	# 				FROM `tabPending Order Roll` por
	# 				WHERE por.`parent`= "{}"
	# 				AND por.`item_code_roll` = "{}"
	# 				AND por.`colour` = "{}"

	# 			""".format(doc.pending_order, i.item_code_roll, i.colour))
	# 			if get_data_pending_order[0][3] :
	# 				temp_qty_dialokasi = get_data_pending_order[0][3]
	# 			else :
	# 				temp_qty_dialokasi = 0

	# 			new_qty_dialokasi = temp_qty_dialokasi - i.roll_qty

	# 			frappe.db.sql ("""
	# 				update 
	# 				`tabPending Order Roll` 
	# 				set 
	# 				qty_dialokasi="{0}"
	# 				where 
	# 				item_code_roll="{1}"
	# 				and 
	# 				colour = "{2}"
					
	# 				""".format(new_qty_dialokasi, i.item_code_roll, i.colour))
					

	# 	if doc.alokasi_barang_pcs :
	# 		for i in doc.alokasi_barang_data :
	# 			get_data_pending_order = frappe.db.sql("""
	# 				SELECT
	# 				por.`pcs_qty`,
	# 				por.`qty_sisa`,
	# 				por.`qty_terkirim`,
	# 				por.`qty_dialokasi`
	# 				FROM `tabPending Order Pcs` por
	# 				WHERE por.`parent`= "{}"
	# 				AND por.`item_code_pcs` = "{}"

	# 			""".format(doc.pending_order, i.item_code_pcs))
	# 			if get_data_pending_order[0][3] :
	# 				temp_qty_dialokasi = get_data_pending_order[0][3]
	# 			else :
	# 				temp_qty_dialokasi = 0

	# 			new_qty_dialokasi = temp_qty_dialokasi - i.pcs_qty

	# 			frappe.db.sql ("""
	# 				update 
	# 				`tabPending Order Roll` 
	# 				set 
	# 				qty_dialokasi="{0}"
	# 				where 
	# 				item_code_pcs="{1}"
					
	# 				""".format(new_qty_dialokasi, i.item_code_pcs))



# @frappe.whitelist()
# def get_data_from_alokasi_barang(source_name, target_doc=None):
# 	def set_missing_values(source, target):
# 		target.pending_order = source.pending_order
# 		target.alokasi_barang = source.name
		

# 	target_doc = get_mapped_doc("Alokasi Barang", source_name, {
# 		"Alokasi Barang": {
# 			"doctype": "Packing List Delivery",
# 			"validation": {
# 				"docstatus": ["=", 1]
# 			}
# 		},
# 		"Alokasi Barang Data": {
# 			"doctype": "Packing List Delivery Data"
# 		},
# 		"Alokasi Barang Pcs": {
# 			"doctype": "Packing List Delivery Pcs"
# 		}
		
# 	}, target_doc, set_missing_values)

# 	return target_doc






@frappe.whitelist()
def get_data_from_alokasi_barang(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.alokasi_barang = source.name
		target.customer = source.customer
		target.customer_name = source.customer_name

		target.sales_partner = source.sales_partner
		if source.sales_type == "Rate" :
			target.total_commission = source.total_commission
		else :
			target.commission_percentage = source.commission_percentage
			target.total_commission = source.total_commission

	def update_item_roll(source_doc, target_doc, source_parent):
		target_doc.alokasi_barang_detail = source_doc.name
		

	def update_item_pcs(source_doc, target_doc, source_parent):
		target_doc.alokasi_barang_detail = source_doc.name



	target_doc = get_mapped_doc("Alokasi Barang", source_name, {
		"Alokasi Barang": {
			"doctype": "Sales Invoice",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Alokasi Barang Data": {
			"doctype": "Sales Invoice Data",
			"postprocess": update_item_roll
		},
		"Alokasi Barang Pcs": {
			"doctype": "Sales Invoice Pcs",
			"postprocess": update_item_pcs
		}
		
	}, target_doc, set_missing_values)

	return target_doc