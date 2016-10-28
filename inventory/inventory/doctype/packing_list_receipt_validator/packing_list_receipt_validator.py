# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

form_grid_templates = {
	"packing_list_data_unchecked": "templates/includes/item_grid_packing_list.html",
	"packing_list_data_checked": "templates/includes/item_grid_packing_list.html",
	"packing_list_data_missing": "templates/includes/item_grid_packing_list.html"
}



class PackingListReceiptValidator(Document):
	def validate_item(self):
		if self.item_code_variant_depan and self.yard_atau_meter and self.colour and self.warehouse and self.qty_roll :
			checker = False
			
			for d in self.get("packing_list_data_unchecked"):
				if d.item_code_variant == self.item_code_variant_depan and d.yard_atau_meter_per_roll == self.yard_atau_meter and d.colour == self.colour and d.warehouse == self.warehouse :
					if self.qty_roll > 0:
						checker = True
						ch = self.append('packing_list_data_checked',{})
						ch.item_code_variant = d.item_code_variant
						ch.item_name = d.item_name
						ch.parent_item = d.parent_item
						ch.yard_atau_meter_per_roll = d.yard_atau_meter_per_roll
						ch.colour = d.colour
						ch.inventory_uom = d.inventory_uom
						ch.group = d.group
						ch.keterangan_group = d.keterangan_group
						ch.warehouse = d.warehouse
						ch.from_data = d.from_data
						
						if self.qty_roll >= d.total_roll :
							ch.total_roll = d.total_roll
							ch.total_yard_atau_meter = d.total_yard_atau_meter
							self.qty_roll = self.qty_roll - ch.total_roll
							self.remove(d)
						else :
							ch.total_roll = self.qty_roll
							ch.total_yard_atau_meter = self.qty_roll * self.yard_atau_meter
							d.total_roll = d.total_roll - self.qty_roll
							d.total_yard_atau_meter = d.total_yard_atau_meter - ch.total_yard_atau_meter
							self.qty_roll = 0
							
							
			if self.qty_roll > 0 :
				if checker :
					frappe.msgprint("Jumlah item melebihi yang tercatat pada Packing List Receipt. Kelebihan akan dimasukkan ke Missing")
				frappe.msgprint("Item tidak ada di dalam Packing List, maka di masukkan ke dalam tabel Missing")
				add_item(self)

			self.yard_atau_meter = 0
			self.qty_roll = 0
			self.colour = ""
				
		else :
			frappe.throw("Data Item belum terisi dengan lengkap")
	
	def validate_pcs(self):
		if self.item_code_pcs and self.warehouse_pcs and self.qty_pcs :
			checker = False
			for d in self.get("packing_list_pcs_unchecked"):
				if d.item_code_pcs == self.item_code_pcs and d.warehouse == self.warehouse_pcs and d.qty_pcs == self.total_pcs :
					if self.qty_pcs > 0 :
						checker = True
						
						ch = self.append('packing_list_pcs_checked',{})
						ch.item_code_pcs = d.item_code_pcs
						ch.item_name_pcs = d.item_name_pcs
						ch.parent_item_pcs = d.parent_item_pcs
						ch.total_pcs = d.total_pcs
						ch.uom_pcs = d.uom_pcs
						ch.warehouse_pcs = d.warehouse_pcs
						ch.from_pcs = d.from_pcs
						
						if self.qty_pcs >= d.total_pcs :
							ch.total_pcs = d.total_pcs
							self.qty_pcs = self.qty_pcs - ch.total_pcs
							self.remove(d)
						else :
							ch.total_pcs = self.qty_pcs
							d.total_pcs = d.total_pcs - self.qty_pcs
							self.qty_pcs = 0
						
					
			if self.qty_pcs > 0 :
				if checker :
					frappe.msgprint("Jumlah item melebihi yang tercatat pada Packing List Receipt. Kelebihan akan dimasukkan ke Missing")
				add_pcs(self)

			self.yard_atau_meter = 0
			self.qty_roll = 0
			self.colour = ""

		else :
			frappe.throw("Data Item belum terisi dengan lengkap")
			
	def return_all_checked(self):
		for d in self.get("packing_list_data_checked") :
			if d.is_return :
				ch = self.append('packing_list_data_unchecked',{})
				ch.item_code_variant = d.item_code_variant
				ch.item_name = d.item_name
				ch.parent_item = d.parent_item
				ch.yard_atau_meter_per_roll = d.yard_atau_meter_per_roll
				ch.colour = d.colour
				ch.inventory_uom = d.inventory_uom
				ch.group = d.group
				ch.keterangan_group = d.keterangan_group
				ch.warehouse = d.warehouse
				ch.from_data = d.from_data
				ch.total_roll = d.total_roll
				ch.total_yard_atau_meter = d.total_yard_atau_meter
				self.remove(d)
		for d in self.get("packing_list_pcs_checked") :
			if d.is_return :
				ch = self.append('packing_list_pcs_unchecked',{})
				ch.item_code_pcs = d.item_code_pcs
				ch.item_name_pcs = d.item_name_pcs
				ch.parent_item_pcs = d.parent_item_pcs
				ch.total_pcs = d.total_pcs
				ch.uom_pcs = d.uom_pcs
				ch.warehouse_pcs = d.warehouse_pcs
				ch.from_pcs = d.from_pcs
					
				self.remove(d)
				
	def on_submit(self):
		if self.get("from_packing_list_receipt") :
			plr = frappe.get_doc("Packing List Receipt",self.get("from_packing_list_receipt"))
			if plr :
				if plr.is_check == 1:
					frappe.throw("Packing List Receipt sudah divalidasi")
				else :
					plr.is_check = 1
			else :
				frappe.throw("Packing List Receipt tidak aka")
		else :
			frappe.throw("Ambil dulu Packing List Receipt")
	
def add_item(self):
	count = 0
	if self.item_code_variant_depan and self.yard_atau_meter and self.colour and self.warehouse :
		master_item = frappe.get_doc("Item", self.item_code_variant_depan)
		parent_item = master_item.variant_of
		item_name = master_item.item_name
		if self.get("packing_list_data_missing") :
			for i in self.packing_list_data_missing :
				if self.group_prefix and self.group_code :
					if i.item_code_variant == self.item_code_variant_depan and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour and i.group == (self.group_prefix+"."+self.group_code) and i.inventory_uom == self.inventory_uom :
						count = 1
				else :
					if i.item_code_variant == self.item_code_variant_depan and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour and i.inventory_uom == self.inventory_uom and i.group == "" :
						count = 1
			if count == 1 :
				for i in self.packing_list_data_missing :
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
					pp_so = self.append('packing_list_data_missing', {})
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
					pp_so = self.append('packing_list_data_missing', {})
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
				pp_so = self.append('packing_list_data_missing', {})
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
				pp_so = self.append('packing_list_data_missing', {})
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
		frappe.throw("Item Code / Colour / Warehouse / Yard / Meter tidak terisi")
		
def add_pcs(self):
	count = 0

	if self.item_code_pcs and self.warehouse_pcs :
		parent_item = frappe.get_doc("Item", self.item_code_pcs).variant_of
		item_name = frappe.get_doc("Item", self.item_code_pcs).item_name
		if self.get("packing_list_pcs_missing") :
			for i in self.packing_list_pcs_missing :
				if i.item_code_pcs == self.item_code_pcs and i.warehouse_pcs == self.warehouse_pcs :
					count = 1

			if count == 1 :
				for i in self.packing_list_pcs_missing :
					if i.item_code_pcs == self.item_code_pcs and i.warehouse_pcs == self.warehouse_pcs :
						new_total_pcs = i.total_pcs
						i.total_pcs = new_total_pcs + self.qty_pcs
			else :
				pp_so = self.append('packing_list_pcs_missing', {})
				pp_so.item_code_pcs = self.item_code_pcs
				pp_so.total_pcs = self.qty_pcs
				pp_so.parent_item_pcs = parent_item
				pp_so.item_name_pcs = item_name
				pp_so.warehouse_pcs = self.warehouse_pcs
				pp_so.uom_pcs = self.uom_pcs

		else :
			pp_so = self.append('packing_list_pcs_missing', {})
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
def get_data_from_packing_list_receipt(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.posting_date = source.posting_date
		target.supplier = source.supplier
		target.supplier_name = source.supplier_name
		target.purchase_order = source.purchase_order
		target.supplier_invoice_no = source.supplier_invoice_no
		target.invoice_date = source.invoice_date
		target.from_packing_list_receipt = source.name

		target.item_code_variant_depan = ""
		target.colour = ""
		target.yard_atau_meter = 0
		target.qty_roll = 0
		target.warehouse = ""
		target.inventory_uom = ""
		target.group_code = ""
		target.keterangan_group = ""

		target.item_code_pcs = ""
		target.uom_pcs = ""
		target.qty_pcs = 0

	def update_item_data(source_doc, target_doc, source_parent):
		target_doc.item_code_variant = source_doc.item_code_variant
		target_doc.item_name = source_doc.item_name
		target_doc.parent_item = source_doc.parent_item
		target_doc.yard_atau_meter_per_roll = source_doc.yard_atau_meter_per_roll
		target_doc.total_roll = source_doc.total_roll
		target_doc.colour = source_doc.colour
		target_doc.total_yard_atau_meter = source_doc.total_yard_atau_meter
		target_doc.inventory_uom = source_doc.inventory_uom
		target_doc.group = source_doc.group
		target_doc.keterangan_group = source_doc.keterangan_group
		target_doc.warehouse = source_doc.warehouse
		target_doc.from_data = source_doc.name
	
	def update_item_pcs(source_doc, target_doc, source_parent):
		target_doc.item_code_pcs = source_doc.item_code_pcs
		target_doc.item_name_pcs = source_doc.item_name_pcs
		target_doc.parent_item_pcs = source_doc.parent_item_pcs
		target_doc.total_pcs = source_doc.total_pcs
		target_doc.uom_pcs = source_doc.uom_pcs
		target_doc.warehouse_pcs = source_doc.warehouse_pcs
		target_doc.from_pcs = source_doc.from_pcs

	target_doc = get_mapped_doc("Packing List Receipt", source_name, {
		"Packing List Receipt": {
			"doctype": "Packing List Receipt Validator",
			"validation": {
				"docstatus": ["=", 1]
			},
		},
		"Packing List Receipt Data": {
			"doctype": "Packing List Receipt Validator Data Unchecked",
			"postprocess": update_item_data
		},
		"Packing List Receipt Data Pcs": {
			"doctype": "Packing List Receipt Validator Pcs Unchecked",
			"postprocess": update_item_pcs
		},
		
	}, target_doc, set_missing_values)

	return target_doc
