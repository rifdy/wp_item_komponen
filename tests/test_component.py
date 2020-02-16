# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase


class MasterComponentTest(TransactionCase):
	def setUp(self):
		super(MasterComponentTest, self).setUp()
		self.component = self.env['wr.komponen']

	def test_component_creates(self):
		comp = self.component.create({'name': 'Component_tes1'})
		search_comp = self.env['wr.komponen'].search([('id', '=', comp.id)], limit=1)
		self.assertTrue(bool(search_comp))
		self.assertTrue(search_comp.waktu_pengerjaan == 0)
