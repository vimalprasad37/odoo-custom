from odoo import models, fields

class Student(models.Model):
    _name = 'student.student'
    _description = 'Student'

    name = fields.Char(string="Full Name")
    roll_no = fields.Integer(string="Roll Number", default=10)
    dob = fields.Date(string="Date of Birth")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")
    course_ids = fields.Many2many(
        'student.course',
        'student_course_rel',
        'student_id',
        'course_id',
        string="Enrolled Courses"
    )
    subject_ids = fields.One2many('student.subject', 'student_id', string="Subjects")
