from odoo import models,fields,api

class StudentResult(models.Model):
    _name = "student.result"
    student_id = fields.Many2one('student.details',string="Student")
    subject = fields.Char(string="Subject")
    teacher = fields.Char(string="Teacher")
    total_marks = fields.Integer(string="Total Marks", default=100)
    obtained_marks = fields.Integer(string="Obtained Marks")
    percentage = fields.Float(string="Percentage",compute="_compute_percentage",digits=(12,2))
    grade = fields.Char(string="Grade", compute="_compute_grade")
    is_first_assessment = fields.Boolean()
    is_second_assessment = fields.Boolean()
    is_final_assessment = fields.Boolean()

    def _compute_percentage(self):
        for record in self:
            if record.obtained_marks and record.total_marks:
                record.percentage = (record.obtained_marks/record.total_marks)*100
            else:
                record.percentage=0
    
    @api.depends('percentage')
    def _compute_grade(self):
        for record in self:
            if record.percentage:
                if record.percentage>=90 and record.percentage<=100:
                    record.grade = 'A'
                elif record.percentage>=80 and record.percentage<90:
                    record.grade = 'B'
                elif record.percentage>=70 and record.percentage<80:
                    record.grade = 'C'
                elif record.percentage>=60 and record.percentage<70:
                    record.grade = 'D'
                elif record.percentage>=50 and record.percentage<60:
                    record.grade = 'E'   
                elif record.percentage<50:
                    record.grade = 'F'
            else:
                record.grade=False



