# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Commission(Document):
	def get_commission(self):
		if self.sales_partner :
			self.commission_item = []
			get_data_group = frappe.db.sql("""
				SELECT
				sinv.`name`,
				sinv.`posting_date`,
				sinv.`customer`,
				sinv.`commission_rate`,
				sinv.`total_commission`
				FROM `tabSales Invoice` sinv
				WHERE sinv.`docstatus` = 1
				AND sinv.`sales_partner` = "{}"
				AND sinv.`commission_used` = 0

			""".format(self.sales_partner))

			if get_data_group :
				for i in get_data_group :
					pp_so = self.append('commission_item', {})
					pp_so.invoice_number = i[0]
					pp_so.customer = i[2]
					pp_so.posting_date = i[1]
					pp_so.commission_value = i[4]
					pp_so.value_from = "Invoice"

		else :
			frappe.throw("Sales Partner belum diisi")
			
	def on_submit(self):
		set_commission_on_submit(self)



@frappe.whitelist()
def save_commission(doc,method):
	total_commission = 0
	for i in doc.commission_item :
		total_commission = total_commission + i.commission_value

	doc.total_commission = total_commission


@frappe.whitelist()
def submit_commission(doc,method):
	
	for data in doc.commission_item :
		frappe.db.sql ("""
				update 
				`tabSales Invoice` 
				set 
				commission_used=1
				where 
				name="{0}"
		
				""".format(data.invoice_number))



@frappe.whitelist()
def cancel_commission(doc,method):
	for data in doc.commission_item :
		frappe.db.sql ("""
				update 
				`tabSales Invoice` 
				set 
				commission_used=0
				where 
				name="{0}"
		
				""".format(data.invoice_number))



@frappe.whitelist()
def make_payment_entry(commission, commission_value):
	je = frappe.new_doc("Journal Entry")
	je.update({
		"voucher_type": "Journal Entry",
		"commission" : commission
	})

	je.append("accounts", {
		"debit_in_account_currency": commission_value
	})

	je.append("accounts", {
		"credit_in_account_currency": commission_value
	})

	return je
	
@frappe.whitelist()
def get_commission_from_invoice(invoice,value_from):
	if value_from == "Invoice" :
		result = frappe.db.sql(""" SELECT i.`total_commission` FROM `tabSales Invoice`i WHERE i.`name`="{0}" """.format(invoice))
		if len(result)==0 :
			return 0
		result = result[0]
		return result[0]
	elif value_from == "Payment" :
		result = frappe.db.sql(""" SELECT i.`commission_rate`,j.`total_amount` FROM `tabSales Invoice`i JOIN `tabPayment Entry Reference`j ON j.`reference_name`=i.`name` WHERE i.`name`="{0}" """.format(invoice))
		if len(result)==0 :
			return 0
		result = result[0]	
		result = result[0] * result[1] / 100
		return result
	else :
		return 0
		
@frappe.whitelist()
def set_commission_on_submit(doc):
	value_clause = ""
	for item in doc.get("commission_item") :
		comm = item.get("commission_value") or 0
		if value_clause == "" :
			value_clause = """ ("{0}", {1}) """.format(item.get("invoice_number"),comm)
		else :
			value_clause = """{0}, ("{1}", {2}) """.format(value_clause,item.get("sales_invoice"),comm)
	
	if value_clause == "" :
		return
	
	frappe.db.sql("""
		INSERT INTO `tabSales Invoice` (`name`, `total_commission`)
		VALUES {0}
		ON DUPLICATE KEY UPDATE 
		`total_commission`=VALUES(`total_commission`)
		""".format(value_clause))