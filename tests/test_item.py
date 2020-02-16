# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase
from datetime import datetime, timedelta
from odoo.exceptions import UserError

class MasterItemTest(TransactionCase):
	def setUp(self):
		super(MasterItemTest, self).setUp()
		self.item = self.env['wr.item']
		self.itemline = self.env['wr.item.line']
		self.komponen = self.env['wr.komponen']

	def test_item_cehck_waktu_mulai_pengerjaan(self):
		data_item = self.item.create({'name': 'Item_tes1'})
		search_item = self.env['wr.item'].search([('id', '=', data_item.id)], limit=1)
		self.assertTrue(bool(search_item))
		self.assertTrue(search_item.tgl_mulai_pengerjaan == datetime.today().strftime('%Y-%m-%d'))
		
	def test_item_cehck_waktu_selesai_ekspektasi(self):
		data_komponen91 = self.komponen.create({'name': 'Komponen 91', 'waktu_pengerjaan': 9})
		data_komponen92 = self.komponen.create({'name': 'Komponen 92', 'waktu_pengerjaan': 4})
		data_komponen93 = self.komponen.create({'name': 'Komponen 93', 'waktu_pengerjaan': 1})
		data_item = self.item.create({'name': 'Item_tes1'})
		search_item = self.env['wr.item'].search([('id', '=', data_item.id)], limit=1)
		data_item_line91 = self.itemline.create({'komponen_id': data_komponen91.id, 'item_id': data_item.id, 'bobot': 2})
		data_item_line92 = self.itemline.create({'komponen_id': data_komponen92.id, 'item_id': data_item.id, 'bobot': 2})
		data_item_line93 = self.itemline.create({'komponen_id': data_komponen93.id, 'item_id': data_item.id, 'bobot': 2})
		self.assertTrue(search_item.tgl_selesai_ekspektasi == (datetime.today() + timedelta(days=int(data_item_line91.komponen_id.waktu_pengerjaan)) + timedelta(days=int(data_item_line92.komponen_id.waktu_pengerjaan)) + timedelta(days=int(data_item_line93.komponen_id.waktu_pengerjaan))).strftime('%Y-%m-%d'))
		
	def test_item_cehck_total_bobot(self):
		data_komponen91 = self.komponen.create({'name': 'Komponen 91', 'waktu_pengerjaan': 9})
		data_komponen92 = self.komponen.create({'name': 'Komponen 92', 'waktu_pengerjaan': 4})
		data_komponen93 = self.komponen.create({'name': 'Komponen 93', 'waktu_pengerjaan': 1})
		data_item = self.item.create({'name': 'Item_tes1'})
		search_item = self.env['wr.item'].search([('id', '=', data_item.id)], limit=1)
		data_item_line91 = self.itemline.create({'komponen_id': data_komponen91.id, 'item_id': data_item.id, 'bobot': 2})
		data_item_line92 = self.itemline.create({'komponen_id': data_komponen92.id, 'item_id': data_item.id, 'bobot': 2})
		data_item_line93 = self.itemline.create({'komponen_id': data_komponen93.id, 'item_id': data_item.id, 'bobot': 2})
		self.assertTrue(search_item.total_bobot == data_item_line91.bobot + data_item_line92.bobot + data_item_line93.bobot)
		
	def test_item_cehck_bobot_persen(self):
		data_komponen91 = self.komponen.create({'name': 'Komponen 91', 'waktu_pengerjaan': 9})
		data_komponen92 = self.komponen.create({'name': 'Komponen 92', 'waktu_pengerjaan': 4})
		data_komponen93 = self.komponen.create({'name': 'Komponen 93', 'waktu_pengerjaan': 1})
		data_item = self.item.create({'name': 'Item_tes1'})
		search_item = self.env['wr.item'].search([('id', '=', data_item.id)], limit=1)
		data_item_line91 = self.itemline.create({'komponen_id': data_komponen91.id, 'item_id': data_item.id, 'bobot': 90})
		data_item_line92 = self.itemline.create({'komponen_id': data_komponen92.id, 'item_id': data_item.id, 'bobot': 10})
		data_item_line93 = self.itemline.create({'komponen_id': data_komponen93.id, 'item_id': data_item.id, 'bobot': 10})
		arr = []
		arr.append(data_item_line91.id)
		arr.append(data_item_line92.id)
		arr.append(data_item_line93.id)
		with self.assertRaises(UserError):
			data_item.write({'item_line_ids': [(6, 0, arr)]})
