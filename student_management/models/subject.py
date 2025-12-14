from odoo import models, fields

class Subject(models.Model):
    _name = 'student.subject'
    _description = 'Subject'

    name = fields.Char(string="Subject Name", required=True)
    marks = fields.Integer(string="Marks", required=True)
    student_id = fields.Many2one('student.student', string="Student")
