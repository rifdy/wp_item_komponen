# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError

class WarungPintarItem(models.TransientModel):
    _name = 'wr.item'

    name = fields.Char(string="Nama Item", required=True)
    item_line_ids = fields.One2many("wr.item.line", "item_id", "Item Line")
    tgl_mulai_pengerjaan = fields.Date(string="Tanggal Mulai Pengerjaan", default=datetime.today())
    tgl_selesai_ekspektasi = fields.Date(string="Ekspektasi Tanggal Selesai", store=True, compute="_hitung_tgl_ekspektasi")
    tgl_selesai_real = fields.Date(string="Real Tanggal Selesai")
    total_bobot = fields.Float(string="Total Bobot Presentase Komponen (%)", store=True, compute="_get_total_bobot")
    
    @api.depends('item_line_ids.komponen_id')
    def _hitung_tgl_ekspektasi(self):
        for wr_items in self:
            tgl_selesai_ekspektasi_temp = datetime.strptime(wr_items.tgl_mulai_pengerjaan, "%Y-%m-%d").date()
            for wr_item_lines in wr_items.item_line_ids:
                tgl_selesai_ekspektasi_temp += timedelta(days=int(wr_item_lines.komponen_id.waktu_pengerjaan))
                wr_items.tgl_selesai_ekspektasi = tgl_selesai_ekspektasi_temp
    
    @api.depends('item_line_ids.bobot')
    def _get_total_bobot(self):
        for wr_items in self:
            temp_bobot = 0.0
            for wr_item_lines in wr_items.item_line_ids:
                if wr_item_lines.bobot:
                    temp_bobot += wr_item_lines.bobot
                    wr_items.total_bobot = temp_bobot
    
    @api.model
    def create(self,vals):
        temp_bobot = 0.0
        check = 0
        result = super(WarungPintarItem, self).create(vals)
        for wr_item_lines in result.item_line_ids:
            if wr_item_lines.bobot:
                temp_bobot += wr_item_lines.bobot
                if temp_bobot > 100:
                    check = 1
        print(temp_bobot)
        if check == 0:
            return result
        else:
            raise UserError('Total Presentase Bobot Melebihi 100%')
        
    @api.multi
    def write(self,vals):
        for itemss in self:
            temp_bobot = 0.0
            check = 0
            result = super(WarungPintarItem, itemss).write(vals)
            for wr_item_lines in itemss.item_line_ids:
                if wr_item_lines.bobot:
                    temp_bobot += wr_item_lines.bobot
                    if temp_bobot > 100:
                        check = 1
            print(temp_bobot)
            if check == 0:
                return result
            else:
                raise UserError('Total Presentase Bobot Melebihi 100%')
