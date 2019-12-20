# -*- coding: utf-8 -*-
# __author__ = 'Linh'

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class OrderLine(models.Model):
    _name = 'order.line'
    _description = ''

    code = fields.Char(related='order_id.code', string='Mã hóa đơn')
    date = fields.Datetime(related='order_id.date', string='Thời gian')
    quantity = fields.Integer(string='Số lượng')
    price = fields.Integer(string='Giá')
    sub_total = fields.Integer(string='Thành tiền', readonly=True)
    state = fields.Selection(related='order_id.state', string='Trạng thái', store=True)

    product_id = fields.Many2one('products', string='Sản phẩm')
    order_id = fields.Many2one(comodel_name='orders', string='Khách hàng')

    # Tính giá khi chọn 1 sản phẩm
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.price = self.product_id.price
            self.quantity = 1

    # Tính tổng tiền
    @api.onchange('quantity', 'price')
    def onchange_total(self):
        self.sub_total = self.quantity * self.price

    @api.multi
    @api.onchange('quantity')
    def check_available(self):
        for line in self:
            if line.quantity > line.product_id.total:
                raise ValidationError("Không đủ hàng trong kho! Chỉ có %s" % line.product_id.total)
