# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase
from datetime import datetime, timedelta
from odoo.exceptions import UserError

class MasterItemLineTest(TransactionCase):
	def setUp(self):
		super(MasterItemLineTest, self).setUp()
		self.item = self.env['wr.item']
		self.itemline = self.env['wr.item.line']
		self.komponen = self.env['wr.komponen']
	
	def test_itemline_name(self):
		data_item = self.item.create({'name': 'Item_tes1'})
		data_komponen91 = self.komponen.create({'name': 'Komponen 91', 'waktu_pengerjaan': 9})
		data_itemline = self.itemline.create({'item_id': data_item.id, 'komponen_id': data_komponen91.id})
		search_itemline = self.env['wr.item.line'].search([('id', '=', data_itemline.id)], limit=1)
		self.assertTrue(bool(search_itemline))
		self.assertTrue(search_itemline.name == str(data_itemline.item_id.name) + "/" + str(data_itemline.komponen_id.name))
	
	def test_itemline_cehck_bobot(self):
		data_itemline = self.itemline.create({'name': 'ItemLine_tes1'})
		search_itemline = self.env['wr.item.line'].search([('id', '=', data_itemline.id)], limit=1)
		self.assertTrue(search_itemline.bobot == 0)
		
	def test_itemline_delete_item(self):
		data_item = self.item.create({'name': 'Item_tes1'})
		data_itemline = self.itemline.create({'item_id': data_item.id})
		data_item.unlink()
		search_itemline = self.env['wr.item.line'].search([('id', '=', data_itemline.id)], limit=1)
		self.assertFalse(bool(search_itemline))

