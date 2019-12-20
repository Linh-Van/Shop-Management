# -*- coding: utf-8 -*-
# __author__ = 'Linh'

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Category(models.Model):
    _name = 'product.category.shop'
    _description = ''

    name = fields.Char(string='Loại')
    product_ids = fields.One2many('products', 'category_ids', string='Sản phẩm')


