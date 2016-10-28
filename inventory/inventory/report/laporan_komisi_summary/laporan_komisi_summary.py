# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	
	columns = ["Sales:Link/Sales Partner:100","Total Invoice:Currency:100","Total Komisi:Currency:100","Total Paid:Currency:100","Total Unpaid:Currency:100"]
	
	data = frappe.db.sql(""" 
		SELECT sales,SUM(total),SUM(total_komisi),SUM(total_paid),SUM(total_komisi)-SUM(total_paid)
		FROM
		(
			SELECT si.`sales_partner` AS sales ,si.`grand_total` AS total,
			CASE WHEN si.`commission_used`=1 THEN ci.`commission_value`
				ELSE si.`total_commission`
				END AS total_komisi,
			CASE WHEN je.`name` IS NULL THEN 0
				WHEN si.`commission_used`=1 THEN ci.`commission_value`
				ELSE si.`total_commission`
				END AS total_paid

			FROM `tabSales Invoice`si
			LEFT JOIN `tabCommission Item`ci ON ci.`invoice_number`=si.`name` AND ci.`docstatus`=1
			LEFT JOIN `tabCommission`c ON c.`name` = ci.`parent` AND c.`docstatus`=1
			LEFT JOIN `tabJournal Entry`je ON je.`commission`=c.`name` AND je.`docstatus`=1 
			
			WHERE si.`docstatus`=1
		) AS sub
		GROUP BY sales
	
		""",as_list=1)
	
	return columns, data
