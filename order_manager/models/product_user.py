# -*- coding: utf-8 -*-
# __author__ = 'Linh'

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductUser(models.Model):
    _name = 'product.user'
    _description = ''

    name = fields.Char(string='Dành cho')
    product_ids = fields.One2many('products', 'product_user_ids', string='Sản phẩm')