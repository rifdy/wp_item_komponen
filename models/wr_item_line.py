# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
# from odoo.exceptions import UserError

class WarungPintarItem(models.TransientModel):
    _name = 'wr.item.line'
    
    name = fields.Char(string="Nama Item Line", store=True, compute="_get_name")
    komponen_id = fields.Many2one("wr.komponen", "Komponen")
    item_id = fields.Many2one("wr.item", "Item", ondelete="cascade")
    bobot = fields.Float(string="Bobot Presentase (%)", default=0)
    
    @api.depends('komponen_id','item_id')
    def _get_name(self):
        for wr_lines in self:
            if wr_lines.item_id.name and wr_lines.komponen_id.name:
                wr_lines.name = str(wr_lines.item_id.name) + "/" + str(wr_lines.komponen_id.name)
