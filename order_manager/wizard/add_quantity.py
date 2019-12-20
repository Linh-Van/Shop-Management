from odoo import models, fields, api


class ResPartnerComment(models.TransientModel):
    _name = 'add.quantity'

    quantity = fields.Integer(string='Thêm số lượng')
    customer_id = fields.Many2one('customer', string='Nhà cung cấp')

    @api.multi
    def add_quantity(self):
        if self.quantity:
            partner_id = self.env.context.get('active_id', False)
            partner = self.env['products'].browse(partner_id)
            partner.total += self.quantity
