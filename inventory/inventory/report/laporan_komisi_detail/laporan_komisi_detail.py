# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	
	columns = ["Sales Partner:Link/Sales Partner:100","Posting Date:Date:100","Invoice No:Link/Sales Invoice:100","Total Invoice:Currency:100","Komisi:Currency:100","Status:Data:100","Paid Date:Date:100"]
	
	date_clause = ""
	if filters.get("from_date") and filters.get("to_date"):
		date_clause = """ AND si.`posting_date` BETWEEN "{0}" AND "{1}" """.format(filters.get("from_date"),filters.get("to_date"))
	
	sales_clause = ""
	if filters.get("sales_partner") :
		sales_clause = """ AND si.`sales_partner`="{0}" """.format(filters.get("sales_partner"))
		
	data = frappe.db.sql("""
		SELECT si.`sales_partner`,si.`posting_date`,si.`name`,si.`grand_total`,
		CASE WHEN si.`commission_used`=1 THEN ci.`commission_value`
			ELSE si.`total_commission`
			END AS commission,
		CASE WHEN je.`name` IS NULL THEN "Unpaid"
			ELSE "Paid"
			END AS stat,
		je.`posting_date`

		FROM `tabSales Invoice`si
		LEFT JOIN `tabCommission Item`ci ON ci.`invoice_number`=si.`name` AND ci.`docstatus`=1
		LEFT JOIN `tabCommission`c ON c.`name` = ci.`parent` AND c.`docstatus`=1
		LEFT JOIN `tabJournal Entry`je ON je.`commission`=c.`name` AND je.`docstatus`=1 
		WHERE si.`docstatus`=1 {0} {1}
		""".format(sales_clause,date_clause),as_list=1)
	
	return columns, data
