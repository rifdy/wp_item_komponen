# -*- coding: utf-8 -*-

from odoo import models, fields

class WarunPintarKomponen(models.Model):
    _name = 'wr.komponen'

    name = fields.Char(string="Nama Komponen", required=True)
    waktu_pengerjaan = fields.Integer(string="Waktu Pengerjaan (Hari)", default=0)
    