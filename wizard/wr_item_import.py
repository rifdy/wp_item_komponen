# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import xlrd
import base64
from io import StringIO
from odoo.exceptions import UserError

class WarungPintarItemImport(models.TransientModel):
    _name = 'wr.item.import'
    excel_file = fields.Binary(string='Excel File', required=True)
     
    @api.multi
    def import_excel(self):
        try:
#             inputx = StringIO()
#             file_data = self.excel_file.decode('base64')
            file_data = base64.decodestring(self.excel_file)
            wb = xlrd.open_workbook(file_contents=file_data)
            sheet = wb.sheet_by_index(0)
            
            total_data = 0
            item_create=False
            for row in range(sheet.nrows):
                col_nama_item = col_tgl_mulai_pekerjaan = col_nama_komponen = col_waktu_pengerjaan = col_bobot = 0
                for col in range(sheet.ncols):
                    if (sheet.cell_value(0, col) == 'Nama Item'):
                        col_nama_item = col
                    elif (sheet.cell_value(0, col) == 'Tanggal Mulai Pengerjaan'):
                        col_tgl_mulai_pekerjaan = col
                    elif (sheet.cell_value(0, col) == 'Nama Komponen'):
                        col_nama_komponen = col
                    elif (sheet.cell_value(0, col) == 'Waktu Pengerjaan Komponen'):
                        col_waktu_pengerjaan = col
                    elif (sheet.cell_value(0, col) == 'Bobot Presentase Komponen'):
                        col_bobot = col 
                if (row > 0):
                    nama_item = tgl_mulai_pekerjaan = nama_komponen = waktu_pengerjaan = bobot = ""
                    if sheet.cell_value(row, col_nama_item):
                        nama_item = str(sheet.cell_value(row, col_nama_item))
                    if sheet.cell_value(row, col_tgl_mulai_pekerjaan):
                        tgl_mulai_pekerjaan_str = float(sheet.cell_value(row, col_tgl_mulai_pekerjaan))
                        tgl_mulai_pekerjaan_datetime = datetime(*xlrd.xldate_as_tuple(tgl_mulai_pekerjaan_str, wb.datemode))
                        tgl_mulai_pekerjaan = tgl_mulai_pekerjaan_datetime.date().isoformat()
                    if sheet.cell_value(row, col_nama_komponen):
                        nama_komponen = str(sheet.cell_value(row, col_nama_komponen))
                    if sheet.cell_value(row, col_waktu_pengerjaan):
                        waktu_pengerjaan = sheet.cell_value(row, col_waktu_pengerjaan)
                    if sheet.cell_value(row, col_bobot):
                        bobot = sheet.cell_value(row, col_bobot)
                    
                    komponen_cek = self.env['wr.komponen'].search([('name','=',nama_komponen)], limit=1)
                    komponen_new=False
                    if not komponen_cek:
                        komponen_new = self.env['wr.komponen'].create({
                            'name': nama_komponen,
                            'waktu_pengerjaan': int(waktu_pengerjaan)
                            })
                    
                    vals={}
                    cek_awal_baris = 0
                    if nama_item: 
                        item_create = self.env['wr.item'].create({
                            'name': nama_item,
                            'tgl_mulai_pengerjaan': tgl_mulai_pekerjaan
                            })
                        vals['item_id'] = item_create.id
                    else:
                        if item_create:
                            vals['item_id'] = item_create.id
                        else:
                            cek_awal_baris = 1
                            print('Baris Awal Tidak ada Nama Item')
                    
                    if komponen_new:
                        vals['komponen_id'] = komponen_new.id
                    else:
                        vals['komponen_id'] = komponen_cek.id
                    vals['bobot'] = float(bobot)
                    if cek_awal_baris == 0:
                        self.env['wr.item.line'].create(vals)
        except Exception as e:
            raise UserError('Gagal Dalam Import Data Employee: %s' %(e))
        
        return True
    