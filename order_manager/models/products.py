# -*- coding: utf-8 -*-
# __author__ = 'Linh'

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import image_resize_images


class Products(models.Model):
    _name = 'products'
    _description = ''

    image = fields.Binary(string='Hình sản phẩm', attachment=True)
    image_medium = fields.Binary(string='Hình sản phẩm', attachment=True)
    image_small = fields.Binary(string='Hình sản phẩm', attachment=True)
    code = fields.Char(string='Mã sản phẩm')
    product_name = fields.Char(string='Tên sản phẩm')
    price = fields.Integer(string='Giá bán')
    stand_price = fields.Integer(string='Giá vốn')
    description = fields.Text(string='Mô tả')
    total = fields.Integer(string='Tổng ', default=0)
    sold = fields.Integer(string='Đã bán', compute='get_sold', default=0, store=True)
    remain = fields.Integer(string='Còn lại ', compute='get_remain', store=True)
    date = fields.Datetime(string='Thời gian tạo', default=lambda self: fields.Datetime.now())

    order_id = fields.Many2one(comodel_name='orders', string='Order')
    order_line_ids = fields.One2many(comodel_name='order.line', inverse_name='product_id',
                                     string='Order line')
    customer_ids = fields.Many2many('customer', string='Nhà cung cấp')
    category_ids = fields.Many2one('product.category.shop', string='Nhóm')
    uom_ids = fields.Many2one('product.uom', string='Đơn vị tính')
    employee_id = fields.Char(string='Người tạo', default=lambda self: self.env.user.name)
    material_ids = fields.Many2one('product.material', string='Chất liệu')
    product_user_ids = fields.Many2one('product.user', string='Dành cho')
    color_ids = fields.Many2one('product.color.att', string='Màu sắc')
    size_ids = fields.Many2one('product.size', string='Size')

    @api.multi
    def name_get(self):
        id_name = [(value.id, "%s/ %s/ %s/ %s" % (value.product_name, value.code, value.size_ids.name, value.material_ids.name)) for value in self]
        return id_name

    @api.multi
    def add_quantity(self):
        if self.quantity:
            partner_id = self.env.context.get('active_id', False)
            partner = self.env['products'].browse(partner_id)
            partner.total += self.quantity

    # Tính số lượng đã bán
    @api.multi
    @api.depends('order_line_ids.quantity', 'order_line_ids.state')
    def get_sold(self):
        for product in self:
            sold = 0
            for line in product.order_line_ids:
                if line.state == 'paid':
                    sold += line.quantity
            product.sold = sold

    # Tính số lượng còn lại trong kho
    @api.depends('total', 'sold')
    def get_remain(self):
        if self.total > 1 and self.total > self.sold:
            self.remain = self.total - self.sold

    @api.multi
    def unlink(self):
        for product in self:
            if product.total >= 1 and self.env.user.name != 'Administrator':
                raise ValidationError('Bạn không có quyền xóa sản phẩm này!\n '
                                      'Vui lòng liên hệ đến quản trị viên!')
            return super(Products, self).unlink()

