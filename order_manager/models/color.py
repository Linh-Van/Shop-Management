# -*- coding: utf-8 -*-
# __author__ = 'Linh'

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductColor(models.Model):
    _name = 'product.color.att'
    _description = ''

    name = fields.Char(string="Màu sắc")
    product_id = fields.One2many('products', 'color_ids', string='Product')
