# -*- coding: utf-8 -*-
# __author__ = 'Linh'

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Customer(models.Model):
    _name = 'customer'
    _description = 'Customer Object Model'

    code = fields.Char(string='Mã', default='#')
    name = fields.Char(string='Tên khách hàng')
    address = fields.Text(string='Địa chỉ')
    phone = fields.Char(string='Di động')
    gender = fields.Selection(selection=[('male', 'Nam'), ('female', 'Nữ')], string='Giới tính')
    order_count = fields.Integer(string='Tổng hóa đơn', default=0, compute='_get_order_count',
                                 store=True)
    is_customer = fields.Boolean(default=True, string='Is a Customer',
                                 help='When tick true is customer')
    is_vendor = fields.Boolean(default=False, string='Is a Vendor', help='When tick true is vendor')

    employee_id = fields.Char(string='Người tạo', default=lambda self: self.env.user.name)
    order_ids = fields.One2many('orders', 'customer_id', string='Danh sách hóa đơn')

    _sql_constraints = [
        ('phone_uniq', 'UNIQUE(phone)',
         'Số điện thoại đã tồn tại. Hãy nhập lại!')
    ]

    # Chuẩn hóa tên và tạo mã tự động
    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('SEQ_CUSTOMER')
        vals['name'] = vals['name'].title()
        return super(Customer, self).create(vals)

    # Đếm số hóa đơn theo khách hàng
    @api.depends('order_ids')
    def _get_order_count(self):
        for customer in self:
            customer.order_count = len(customer.order_ids)

    # Báo lỗi xóa khách hàng
    @api.multi
    def unlink(self):
        for customer in self:
            if customer.name and self.env.user.name != 'Administrator':
                raise ValidationError('Bạn không có quyền xóa khách hàng!\n '
                                      'Vui lòng liên hệ đến quản trị viên!')
        return super(Customer, self).unlink()
