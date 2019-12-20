# -*- coding: utf-8 -*-
# __author__ = 'Linh'

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Uom(models.Model):
    _name = 'product.uom'
    _description = ''

    name = fields.Char(string='Đơn vị tính')
    product_ids = fields.One2many('products', 'uom_ids', string='Sản phẩm')
