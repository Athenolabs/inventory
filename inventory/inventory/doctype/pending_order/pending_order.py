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
	"pending_order_roll": "templates/includes/pending_order.html",
	"pending_order_group_temp": "templates/includes/pending_order_group_temp.html"
}

class PendingOrder(Document):
	def get_data_group(self):
		
		if self.pending_order_group_temp :
			for dg in self.pending_order_group_temp :
				count = 0
				item = frappe.get_doc("Item", dg.item_code_variant)
				if self.pending_order_roll :
					for i in self.pending_order_roll :
						if i.item_code_roll == dg.item_code_variant and i.colour == dg.colour and i.warehouse == item.default_warehouse :
							count = 1

					if count == 1 :
						for i in self.pending_order_roll :
							if i.item_code_roll == dg.item_code_variant and i.colour == dg.colour and i.warehouse == item.default_warehouse :
								new_total_roll = i.roll_qty
								i.roll_qty = new_total_roll + dg.total_roll
								new_total_rate = i.total_rate
								i.total_rate = new_total_rate + (dg.total_roll * i.rate)

					else :
						pp_so = self.append('pending_order_roll', {})
						pp_so.item_code_roll = dg.item_code_variant
						pp_so.item_name_roll = item.item_name
						pp_so.colour = dg.colour
						pp_so.roll_qty = dg.total_roll
						
						pp_so.qty_dialokasi = 0
						pp_so.qty_terkirim = 0
						pp_so.rate = dg.rate
						pp_so.total_rate = dg.rate * dg.total_roll
						pp_so.warehouse = item.default_warehouse

				else :
					pp_so = self.append('pending_order_roll', {})
					pp_so.item_code_roll = dg.item_code_variant
					pp_so.item_name_roll = item.item_name
					pp_so.colour = dg.colour
					pp_so.roll_qty = dg.total_roll
					
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
				AND dg.`is_used` = 0
				order by dg.`idx`, dg.`colour`

			""".format(self.group_item))


			if get_data_group :
				for dg in get_data_group :
						
					pp_so = self.append('pending_order_group_temp', {})
					pp_so.item_code_variant = dg[2]
					pp_so.colour = dg[5]
					pp_so.total_roll = dg[9]
					pp_so.yard_atau_meter_per_roll = dg[6]

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

					if qty_terkirim == 0 :
						pp_so.qty_terkirim = 0
					else :
						pp_so.qty_terkirim = qty_terkirim

					if qty_dialokasi == 0 :
						pp_so.qty_alokasi_barang = 0
					else :
						pp_so.qty_alokasi_barang = qty_dialokasi - pp_so.qty_terkirim

					
					if qty_pending_order == 0 :
						pp_so.qty_pending_order = 0
					else :
						pp_so.qty_pending_order = qty_pending_order - pp_so.qty_alokasi_barang
					

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
				if self.pending_order_pcs :
					if self.qty_pcs > self.jumlah_di_stock :
						msgprint("Qty yang akan di inputkan lebih besar daripada yang ada di Inventory")

					for i in self.pending_order_pcs :
						if i.item_code_pcs == self.item_code_pcs and i.warehouse == self.warehouse_pcs and i.rate == self.rate_pcs :
							new_total_roll = i.pcs_qty
							i.pcs_qty = new_total_roll + self.qty_pcs

							

							new_total_rate = i.total_rate
							i.total_rate = new_total_rate + (self.qty_pcs * self.rate_pcs)
						else :
							pp_so = self.append('pending_order_pcs', {})
							pp_so.item_code_pcs = self.item_code_pcs
							pp_so.item_name_roll = self.item_name_pcs
							pp_so.pcs_qty = self.qty_pcs
							
							pp_so.qty_dialokasi = 0
							pp_so.qty_terkirim = 0
							pp_so.rate = self.rate_pcs
							pp_so.total_rate = self.rate_pcs * self.qty_pcs
							pp_so.warehouse = self.warehouse_pcs
				else :
					pp_so = self.append('pending_order_pcs', {})
					pp_so.item_code_pcs = self.item_code_pcs
					pp_so.item_name_roll = self.item_name_pcs
					pp_so.pcs_qty = self.qty_pcs
					
					pp_so.qty_dialokasi = 0
					pp_so.qty_terkirim = 0
					pp_so.rate = self.rate_pcs
					pp_so.total_rate = self.rate_pcs * self.qty_pcs
					pp_so.warehouse = self.warehouse_pcs


			self.rate = 0
			self.qty = 0

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
						msgprint("Qty yang akan di inputkan lebih besar daripada yang ada di Inventory")
					if self.pending_order_roll :
						for i in self.pending_order_roll :
							if i.item_code_roll == self.item_code and i.colour == self.colour_pending_order and i.warehouse == self.warehouse and i.rate == self.rate :
								count = 1

						if count == 1 :
							for i in self.pending_order_roll :
								if i.item_code_roll == self.item_code and i.colour == self.colour_pending_order and i.warehouse == self.warehouse and i.rate == self.rate :
									new_total_roll = i.roll_qty
									i.roll_qty = new_total_roll + self.qty
									new_total_rate = i.total_rate
									i.total_rate = new_total_rate + (self.qty * self.rate)

									new_total_yard = i.total_yard
									i.total_yard = new_total_yard + self.total_yard

						else :
							pp_so = self.append('pending_order_roll', {})
							pp_so.item_code_roll = self.item_code
							pp_so.item_name_roll = self.item_name
							pp_so.colour = self.colour_pending_order
							pp_so.roll_qty = self.qty
							pp_so.total_yard = self.total_yard
							
							pp_so.qty_dialokasi = 0
							pp_so.qty_terkirim = 0
							pp_so.rate = self.rate
							pp_so.total_rate = self.rate * self.qty
							pp_so.warehouse = self.warehouse
					
					else :
						pp_so = self.append('pending_order_roll', {})
						pp_so.item_code_roll = self.item_code
						pp_so.item_name_roll = self.item_name
						pp_so.colour = self.colour_pending_order
						pp_so.roll_qty = self.qty
						pp_so.total_yard = self.total_yard
						
						pp_so.qty_dialokasi = 0
						pp_so.qty_terkirim = 0
						pp_so.rate = self.rate
						pp_so.total_rate = self.rate * self.qty
						pp_so.warehouse = self.warehouse


					
					self.colour_pending_order = ""
					self.rate = 0
					self.qty = 0
					self.total_yard = 0
					

					self.jumlah_di_inventory = 0
					self.jumlah_alokasi_barang = 0
					self.jumlah_di_pending_order = 0

				else :
					frappe.throw("Colour tidak ada isinya")

			# elif self.uom == "Pcs" :
			# 	if self.pending_order_pcs :
			# 		if self.qty > self.jumlah_di_inventory :
			# 			msgprint("Qty yang akan di inputkan lebih besar daripada yang ada di Inventory")

			# 		for i in self.pending_order_pcs :
			# 			if i.item_code_pcs == self.item_code and i.warehouse == self.warehouse and i.rate == self.rate :
			# 				new_total_roll = i.pcs_qty
			# 				i.pcs_qty = new_total_roll + self.qty

							

			# 				new_total_rate = i.total_rate
			# 				i.total_rate = new_total_rate + (self.qty * self.rate)
			# 			else :
			# 				pp_so = self.append('pending_order_pcs', {})
			# 				pp_so.item_code_pcs = self.item_code
			# 				pp_so.item_name_roll = self.item_name
			# 				pp_so.pcs_qty = self.qty
							
			# 				pp_so.qty_dialokasi = 0
			# 				pp_so.qty_terkirim = 0
			# 				pp_so.rate = self.rate
			# 				pp_so.total_rate = self.rate * self.qty
			# 				pp_so.warehouse = self.warehouse
			# 	else :
			# 		pp_so = self.append('pending_order_pcs', {})
			# 		pp_so.item_code_pcs = self.item_code
			# 		pp_so.item_name_roll = self.item_name
			# 		pp_so.pcs_qty = self.qty
					
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
def save_pending_order(doc,method):
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

	if doc.pending_order_roll :
		for i in doc.pending_order_roll :
			i.total_rate = i.roll_qty * i.rate
			total_rate = total_rate + i.total_rate
			i.qty_sisa = i.roll_qty
			

	if doc.pending_order_pcs :
		for i in doc.pending_order_pcs :
			i.total_rate = i.pcs_qty * i.rate
			total_rate = total_rate + i.total_rate
			i.qty_sisa = i.pcs_qty
			

	doc.grand_total = total_rate
	doc.outstanding_amount = total_rate
	if doc.sales_type == "%" :
		doc.total_commission = total_rate * doc.commission_percentage / 100
	else :
		doc.total_commission = doc.commission_rate



# @frappe.whitelist()
# def get_data_from_pending_order(resep):
# 	query = """
# 		SELECT
# 		po.`name`,
# 		po.`posting_date`,
# 		po.`expected_delivery_date`,
# 		po.`customer`,
# 		po.`customer_name`,
# 		po.`note`,
# 		po.`sales_partner`,
# 		po.`sales_type`,
# 		po.`commision_percentage`,
# 		po.`commision_rate`

# 		FROM `tabPending Order` po
# 		WHERE po.`name` = "{}"
# 		"""

# 	items = frappe.db.sql(query, { "resep": resep }, as_dict=True)


# 	return items




@frappe.whitelist()
def get_data_from_pending_order(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.pending_order = source.name
		target.item_code = ""
		target.item_name = ""
		target.colour_pending_order = ""
		target.uom = ""
		target.warehouse = ""
		target.rate = ""
		
		target.qty = ""
		target.jumlah_di_inventory = ""
		target.jumlah_di_pending_order = ""
		target.jumlah_alokasi_barang = ""
		target.group_item = ""

		target.total_commission = ""
		target.grand_total = ""
		target.outstanding_amount = ""

		target.pending_order_group_temp = []
		target.keterangan_group = ""

	def update_item_roll(source, target, source_parent):
		target.total_rate = flt(source.qty_sisa) * flt(source.rate)
		target.roll_qty = flt(source.qty_sisa)

	def update_item_pcs(source, target, source_parent):
		target.total_rate = flt(source.qty_sisa) * flt(source.rate)
		target.pcs_qty = flt(source.qty_sisa)

	target_doc = get_mapped_doc("Pending Order", source_name, {
		"Pending Order": {
			"doctype": "Alokasi Barang",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Pending Order Roll": {
			"doctype": "Summary Pending Order",
			"postprocess": update_item_roll,
			"condition": lambda doc: abs(doc.qty_sisa) > 0
		},
		"Pending Order Pcs": {
			"doctype": "Summary Pending Order Pcs",
			"postprocess": update_item_pcs,
			"condition": lambda doc: abs(doc.qty_sisa) > 0
		}
		
	}, target_doc, set_missing_values)

	return target_doc

@frappe.whitelist()
def change_status_document_and_child(name,status_document,type):
	cur_status = frappe.get_value(type,name,"status_document")
	if cur_status == status_document :
		return ""
	frappe.db.sql(""" UPDATE `tab{0}`i SET i.`status_document`="{1}" WHERE i.`name`="{2}" """.format(type,status_document,name))
	frappe.db.sql(""" UPDATE `tab{0} Pcs`p1, `tab{0} Pcs`p2 SET p1.`qty_sisa`=p2.`old_sisa`, p1.`old_sisa`= p2.`qty_sisa`
		WHERE p1.`name`=p2.`name` AND p1.`parent`="{1}" """.format(type,name))
	if type == "Pending Order" :
		frappe.db.sql(""" UPDATE `tab{0} Roll`r1, `tab{0} Roll`r2 SET r1.`qty_sisa`=r2.`old_sisa`, r1.`old_sisa`=r2.`qty_sisa`
			WHERE r1.`name`=r2.`name` AND r1.`parent`="{1}" """.format(type,name))
	elif type=="Alokasi Barang":
		frappe.db.sql(""" UPDATE `tab{0} Data`r1, `tab{0} Data`r2 SET r1.`qty_sisa`=r2.`old_sisa`, r1.`old_sisa`=r2.`qty_sisa`
			WHERE r1.`name`=r2.`name` AND r1.`parent`="{1}" """.format(type,name))
	frappe.db.commit();
	return ""


@frappe.whitelist()
def duplicate_sisa(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.duplicate_from = source.name
		target.status_document = "Open"
	
	def update_item_roll(source, target, source_parent):
		target.total_rate = flt(source.qty_sisa) * flt(source.rate)
		target.roll_qty = flt(source.qty_sisa)

	def update_item_pcs(source, target, source_parent):
		target.total_rate = flt(source.qty_sisa) * flt(source.rate)
		target.pcs_qty = flt(source.qty_sisa)


	target_doc = get_mapped_doc("Pending Order", source_name, {
		"Pending Order": {
			"doctype": "Pending Order",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Pending Order Roll": {
			"doctype": "Pending Order Roll",
			"postprocess": update_item_roll,
			"condition": lambda doc: abs(doc.qty_sisa) > 0
		},
		"Pending Order Pcs": {
			"doctype": "Pending Order Pcs",
			"postprocess": update_item_pcs,
			"condition": lambda doc: abs(doc.qty_sisa) > 0
		}
		
	}, target_doc, set_missing_values)


	return target_doc


@frappe.whitelist()
def submit_pending_order_duplicate(doc,method):
	if doc.duplicate_from :
		po_before = doc.duplicate_from
		frappe.db.sql(""" UPDATE `tabPending Order`i SET i.`status_document`="{0}" WHERE i.`name`="{1}" """.format("Close",po_before))
		if doc.pending_order_roll :
			frappe.db.sql(""" 
				UPDATE `tabPending Order Roll`r1, `tabPending Order Roll`r2 
				SET r1.`qty_sisa`=r2.`old_sisa`, r1.`old_sisa`=r2.`qty_sisa`
				WHERE r1.`name`=r2.`name` 
				AND r1.`parent`="{0}" 
				""".format(po_before))

		if doc.pending_order_pcs :
			frappe.db.sql(""" 
				UPDATE `tabPending Order Pcs`p1, `tabPending Order Pcs`p2 
				SET p1.`qty_sisa`=p2.`old_sisa`, p1.`old_sisa`= p2.`qty_sisa`
				WHERE p1.`name`=p2.`name` 
				AND p1.`parent`="{0}" """.format(po_before))


@frappe.whitelist()
def cancel_pending_order_duplicate(doc,method):
	if doc.duplicate_from :
		po_before = doc.duplicate_from
		frappe.db.sql(""" UPDATE `tabPending Order`i SET i.`status_document`="{0}" WHERE i.`name`="{1}" """.format("Open",po_before))
		if doc.pending_order_roll :
			frappe.db.sql(""" 
				UPDATE `tabPending Order Roll`r1, `tabPending Order Roll`r2 
				SET r1.`qty_sisa`=r2.`old_sisa`, r1.`old_sisa`=r2.`qty_sisa`
				WHERE r1.`name`=r2.`name` 
				AND r1.`parent`="{0}" 
				""".format(po_before))

		if doc.pending_order_pcs :
			frappe.db.sql(""" 
				UPDATE `tabPending Order Pcs`p1, `tabPending Order Pcs`p2 
				SET p1.`qty_sisa`=p2.`old_sisa`, p1.`old_sisa`= p2.`qty_sisa`
				WHERE p1.`name`=p2.`name` 
				AND p1.`parent`="{0}" """.format(po_before))
