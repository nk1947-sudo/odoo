
from odoo import models, fields

class TenderDepartment(models.Model):
    _name = 'tender.department'
    _description = 'Tender Department'
    _rec_name = 'name'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    description = fields.Text()
