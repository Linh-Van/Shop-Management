# -*- coding: utf-8 -*-
# __author__ = 'Linh'

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Size(models.Model):
    _name = 'product.size'
    _description = ''

    name = fields.Char(string='Size')
    product_ids = fields.One2many('products', 'size_ids', string='')
