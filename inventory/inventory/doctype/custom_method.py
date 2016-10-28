# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import msgprint

class custom_method(Document):
	pass


@frappe.whitelist()
def insert_invoice_summary(doc, method):
	
	if doc.is_return == 1 :
		sales_invoice_return = doc.name
		return_against = doc.return_against

		mi = frappe.get_doc("Sales Invoice", doc.return_against)
		mi.append("invoice_summary", {
			"doctype": "Invoice Summary",
			"type" : "Sales Invoice",
			"type_code" : doc.name,
			"date" : doc.posting_date
		})

		mi.flags.ignore_permissions = 1
		mi.save()



@frappe.whitelist()
def validate_item_colour(doc, method):
	if doc.colour :
		count = 0

		split_colour = doc.colour.split("\n")

		for c in split_colour :
			
			check_colour = frappe.db.sql("""
				SELECT c.`name` 
				FROM `tabColour` c
				WHERE c.`name` = "{}"
			""".format(c))

			if check_colour :
				count = 1
			else :
				pr_doc = frappe.new_doc("Colour")
				pr_doc.update({
					"colour": c
				})
				pr_doc.flags.ignore_permissions = 1
				pr_doc.save()


@frappe.whitelist()
def divide_group(item_code_variant):
	
	group = item_code_variant.split(" ")[0]

	return group



# @frappe.whitelist()
# def projected_stock_by_item_pcs(item_code):

		# qty_pending_order = 0
		# qty_terkirim = 0
		# qty_dialokasi = 0
		# qty_inventory = 0

		# uom = frappe.get_doc("Item",item_code).stock_uom


		# get_qty_pending_order = frappe.db.sql("""
		# 	SELECT
		# 	SUM(por.`pcs_qty`)

		# 	FROM `tabPending Order` po
		# 	JOIN `tabPending Order Pcs` por
		# 	ON po.`name` = por.`parent`
		# 	WHERE po.`docstatus` < 2
		# 	AND por.`docstatus` < 2
		# 	AND por.`item_code_pcs` = "{}"
		# 	GROUP BY por.`item_code_pcs`
		# 	""".format(item_code))


		# get_qty_terkirim = frappe.db.sql("""
		# 	SELECT
		# 	SUM(por.`qty_terkirim`)

		# 	FROM `tabPending Order` po
		# 	JOIN `tabPending Order Pcs` por
		# 	ON po.`name` = por.`parent`
		# 	WHERE po.`docstatus` < 2
		# 	AND por.`docstatus` < 2
		# 	AND por.`item_code_pcs` = "{}"
		# 	GROUP BY por.`item_code_pcs`
		# 	""".format(item_code))



		# get_qty_dialokasi = frappe.db.sql("""
		# 	SELECT
		# 	SUM(por.`qty_dialokasi`)

		# 	FROM `tabPending Order` po
		# 	JOIN `tabPending Order Pcs` por
		# 	ON po.`name` = por.`parent`
		# 	WHERE po.`docstatus` < 2
		# 	AND por.`docstatus` < 2
		# 	AND por.`item_code_pcs` = "{}"
		# 	GROUP BY por.`item_code_pcs`
		# 	""".format(item_code))



		# # bukan dari inventory karena pcs tetapi ambil dari tab Bin
		# get_qty_inventory = frappe.db.sql("""
		# 	SELECT
		# 	SUM(b.`actual_qty`)
		# 	FROM `tabBin` b
		# 	WHERE b.`item_code` = "{}"
		# 	GROUP BY b.`item_code`
		# 	""".format(item_code))



		# if get_qty_pending_order :
		# 	qty_pending_order = float(get_qty_pending_order[0][0])
		# else :
		# 	qty_pending_order = 0


		# if get_qty_terkirim :
		# 	qty_terkirim = float(get_qty_terkirim[0][0])
		# else :
		# 	qty_terkirim = 0


		# if get_qty_dialokasi :
		# 	qty_dialokasi = float(get_qty_dialokasi[0][0])
		# else :
		# 	qty_dialokasi = 0


		# if get_qty_inventory :
		# 	qty_inventory = float(get_qty_inventory[0][0])
		# else :
		# 	qty_inventory = 0

		# send_data = []
		# temp_qty_pending_order = qty_pending_order - qty_dialokasi - qty_terkirim
		# temp_qty_dialokasi = qty_dialokasi
		# temp_qty_terkirim = qty_terkirim
		# temp_qty_inventory = qty_inventory - qty_dialokasi - (qty_pending_order - qty_dialokasi - qty_terkirim)

		# send_data.append(str(temp_qty_pending_order))
		# send_data.append(str(temp_qty_dialokasi))
		# send_data.append(str(temp_qty_terkirim))
		# send_data.append(str(temp_qty_inventory))


	

# 	return send_data





@frappe.whitelist()
def projected_stock_by_item(item_code, colour):
	uom = frappe.get_doc("Item",item_code).stock_uom

	if uom == "Pcs" :
		qty_pending_order = 0
		qty_terkirim = 0
		qty_dialokasi = 0
		qty_inventory = 0

		get_qty_pending_order = frappe.db.sql("""
			SELECT
			SUM(por.`pcs_qty`)

			FROM `tabPending Order` po
			JOIN `tabPending Order Pcs` por
			ON po.`name` = por.`parent`
			WHERE po.`docstatus` < 2
			AND por.`docstatus` < 2
			AND por.`item_code_pcs` = "{}"
			GROUP BY por.`item_code_pcs`
			""".format(item_code))

		get_qty_terkirim = frappe.db.sql("""
			SELECT
			SUM(por.`pcs_qty`)

			FROM `tabPacking List Delivery` po
			JOIN `tabPacking List Delivery Pcs` por
			ON po.`name` = por.`parent`
			WHERE po.`docstatus` < 2
			AND por.`docstatus` < 2
			AND por.`item_code_pcs` = "{}"
			GROUP BY por.`item_code_pcs`
			""".format(item_code))

		get_qty_dialokasi = frappe.db.sql("""
			SELECT
			SUM(por.`pcs_qty`)

			FROM `tabAlokasi Barang` po
			JOIN `tabAlokasi Barang Pcs` por
			ON po.`name` = por.`parent`
			WHERE po.`docstatus` < 2
			AND por.`docstatus` < 2
			AND por.`item_code_pcs` = "{}"
			GROUP BY por.`item_code_pcs`
			""".format(item_code))

		# bukan dari inventory karena pcs tetapi ambil dari tab Bin
		get_qty_inventory = frappe.db.sql("""
			SELECT
			SUM(b.`actual_qty`)
			FROM `tabBin` b
			WHERE b.`item_code` = "{}"
			GROUP BY b.`item_code`
			""".format(item_code))


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

		send_data = []
		if qty_terkirim == 0 :
			temp_qty_terkirim = 0
		else :
			temp_qty_terkirim = qty_terkirim

		if qty_dialokasi == 0 :
			temp_qty_dialokasi = 0
		else :
			temp_qty_dialokasi = qty_dialokasi - temp_qty_terkirim


		if qty_pending_order == 0 :
			temp_qty_pending_order = 0
		else :
			temp_qty_pending_order = qty_pending_order - temp_qty_dialokasi


		if qty_inventory == 0 :
			temp_qty_inventory = 0
		else :
			temp_qty_inventory = qty_inventory - temp_qty_dialokasi

		send_data.append(str(temp_qty_pending_order))
		send_data.append(str(temp_qty_dialokasi))
		send_data.append(str(temp_qty_terkirim))
		send_data.append(str(temp_qty_inventory))

		return send_data

	else :
		qty_pending_order = 0
		qty_terkirim = 0
		qty_dialokasi = 0
		qty_inventory = 0

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
			""".format(item_code, colour))

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
			GROUP BY por.`item_code_roll`
			""".format(item_code, colour))

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
			GROUP BY por.`item_code_roll`
			""".format(item_code, colour))

		get_qty_inventory = frappe.db.sql("""
			SELECT
			SUM(di.`total_roll`)
			FROM `tabData Inventory` di
			WHERE di.`item_code_variant` = "{}"
			AND di.`colour` = "{}"

			GROUP BY di.`item_code_variant`
			""".format(item_code, colour))

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

		send_data = []

		if qty_terkirim == 0 :
			temp_qty_terkirim = 0
		else :
			temp_qty_terkirim = qty_terkirim

		if qty_dialokasi == 0 :
			temp_qty_dialokasi = 0
		else :
			temp_qty_dialokasi = qty_dialokasi - temp_qty_terkirim


		if qty_pending_order == 0 :
			temp_qty_pending_order = 0
		else :
			temp_qty_pending_order = qty_pending_order - temp_qty_dialokasi
		


		if qty_inventory == 0 :
			temp_qty_inventory = 0
		else :
			temp_qty_inventory = qty_inventory - temp_qty_dialokasi


		send_data.append(str(temp_qty_pending_order))
		send_data.append(str(temp_qty_dialokasi))
		send_data.append(str(temp_qty_terkirim))
		send_data.append(str(temp_qty_inventory))

		return send_data




@frappe.whitelist()
def projected_stock_by_colour(item_code, colour):

	qty_pending_order = 0
	qty_terkirim = 0
	qty_dialokasi = 0
	qty_inventory = 0

	uom = frappe.get_doc("Item",item_code).stock_uom

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
		""".format(item_code, colour))

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
		GROUP BY por.`item_code_roll`
		""".format(item_code, colour))

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
		GROUP BY por.`item_code_roll`
		""".format(item_code, colour))

	get_qty_inventory = frappe.db.sql("""
		SELECT
		SUM(di.`total_roll`)
		FROM `tabData Inventory` di
		WHERE di.`item_code_variant` = "{}"
		AND di.`colour` = "{}"

		GROUP BY di.`item_code_variant`
		""".format(item_code, colour))


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

	send_data = []
	if qty_terkirim == 0 :
		temp_qty_terkirim = 0
	else :
		temp_qty_terkirim = qty_terkirim

	if qty_dialokasi == 0 :
		temp_qty_dialokasi = 0
	else :
		temp_qty_dialokasi = qty_dialokasi - temp_qty_terkirim


	if qty_pending_order == 0 :
		temp_qty_pending_order = 0
	else :
		temp_qty_pending_order = qty_pending_order - temp_qty_dialokasi




	if qty_inventory == 0 :
		temp_qty_inventory = 0
	else :
		temp_qty_inventory = qty_inventory - temp_qty_dialokasi

	send_data.append(str(temp_qty_pending_order))
	send_data.append(str(temp_qty_dialokasi))
	send_data.append(str(temp_qty_terkirim))
	send_data.append(str(temp_qty_inventory))

	return send_data