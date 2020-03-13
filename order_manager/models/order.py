# -*- coding: utf-8 -*-
# __author__ = 'Linh'

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Order(models.Model):
    _name = 'orders'
    _description = ''
    _rec_name = 'customer_id'

    code = fields.Char(string='Mã hóa đơn')
    date = fields.Datetime(string='Thời gian', default=lambda self: fields.Datetime.now())
    total_amount = fields.Float(string='Tổng cộng', compute='_get_total_amount', store=True)
    note = fields.Text(string='Ghi chú')
    state = fields.Selection(selection=[('draft', 'Chưa xác nhận'), ('paid', 'Đã thanh toán')],
                             string='Trạng thái', default='draft')

    customer_id = fields.Many2one(comodel_name='customer', string='Khách hàng')
    employee_id = fields.Char(string='Người lập hóa đơn', default=lambda self: self.env.user.name)
    line_ids = fields.One2many(comodel_name='order.line', inverse_name='order_id',
                               string='Hóa đơn chi tiết')
    product_ids = fields.One2many(comodel_name='products', inverse_name='order_id',
                                  string='Product')

    # Tạo mã tự động
    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('SEQ_ORDER')
        return super(Order, self).create(vals)

    # Tính thành tiền
    @api.multi
    @api.depends('line_ids.sub_total')
    def _get_total_amount(self):
        for order in self:
            total_amount = 0
            for line in order.line_ids:
                total_amount += line.sub_total
            order.total_amount = total_amount

    # Chuyển trạng thái hóa đơn
    @api.multi
    def validate_order(self):
        if self.total_amount > 0:
            self.state = 'paid'
        if self.line_ids == False:
            raise ValidationError('Chưa có sản phẩm trong hóa đơn!')

    # Báo lỗi xóa hóa đơn trạng thái 'paid'
    @api.multi
    def unlink(self):
        for order in self:
            if order.state == 'paid' and self.env.user.name != 'Administrator':
                raise ValidationError('Bạn không có quyền xóa hóa đơn đã thanh toán!\n '
                                      'Vui lòng liên hệ đến quản trị viên!')
        return super(Order, self).unlink()
    # day la doan test git
    # cmt on github
    # thu lay code
    ############3bdabajsagjjavjabqjegqegqwqgjhhhasssssssssssssse3342423342323432

#drhhhhhhhhhhhhhh8438242y4234y2uasdms h
########amhkadakdaidssakdsds
amasasdadkadaskdasbkdaskdakda