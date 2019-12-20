# -*- coding: utf-8 -*-
# __author__ = 'Linh'

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Material(models.Model):
    _name = 'product.material'
    _description = ''

    name = fields.Char(string='Chất liệu')
    product_id = fields.One2many('products', 'material_ids', string='')
