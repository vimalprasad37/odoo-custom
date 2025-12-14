from odoo import models, fields

class Course(models.Model):
    _name = 'student.course'
    _description = 'Course'

    name = fields.Char(string="Course Name", required=True)
    code = fields.Char(string="Course Code", required=True)
    duration = fields.Integer(string="Duration (months)")
    student_ids = fields.Many2many(
        'student.student',
        'student_course_rel',
        'course_id',
        'student_id',
        string="Students"
    )
