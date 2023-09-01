from odoo import models,api,fields,_
import re
from odoo.exceptions import ValidationError

class StudentDetails(models.Model):
    _name = "student.details"
    def _compute_display_name(self):
        for record in self:
            if record.rollno:
                record.display_name = record.name + " - " + record.rollno
            else:
                record.display_name = record.name
    name = fields.Char(string="Name")
    photo = fields.Binary(string="Photo")
    email = fields.Char(string='Email address')
    father_name = fields.Char(string='Father Name')
    mother_name = fields.Char(string='Mother Name')
    mobile_no = fields.Char(string="Mobile No")
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    state = fields.Many2one('res.country.state', 'State', domain="[('country_id', '=?', country)]")
    country = fields.Many2one('res.country', string="Country")
    rollno = fields.Char(string="Roll No", readonly=True)
    class_name = fields.Char(string="Class")
    course = fields.Char(string="Course")
    first_results = fields.One2many('student.result','student_id',string="First Assessment Results", domain=[('is_first_assessment','=',True)])
    second_results = fields.One2many('student.result','student_id',string="Second Assessment Results", domain=[('is_second_assessment','=',True)])
    final_results = fields.One2many('student.result','student_id',string="Final Assessment Results", domain=[('is_final_assessment','=',True)])
    
    first_total = fields.Integer(string="Total Marks",compute="_compute_total_percentage_grade")
    second_total = fields.Integer(string="Total Marks",compute="_compute_total_percentage_grade")
    final_total = fields.Integer(string="Total Marks",compute="_compute_total_percentage_grade")

    first_percentage = fields.Float(string="Total Percentage",compute="_compute_total_percentage_grade", digits=(12,2))
    second_percentage = fields.Float(string="Total Percentage",compute="_compute_total_percentage_grade",digits=(12,2))
    final_percentage = fields.Float(string="Total Percentage",compute="_compute_total_percentage_grade",digits=(12,2))

    first_grade = fields.Char(string="Overall Grade", compute="_compute_total_percentage_grade")
    second_grade = fields.Char(string="Overall Grade", compute="_compute_total_percentage_grade")
    final_grade = fields.Char(string="Overall Grade", compute="_compute_total_percentage_grade")

    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Please Enter a valid Email ID!')
            
    @api.onchange('mobile_no')
    def validate_mobile_no(self):
        if self.mobile_no:
            if len(self.mobile_no)==10:
                try:
                    mobile = int(self.mobile_no)
                except:
                    raise ValidationError('Mobile number should only contain numbers(0-9) and be exactly 10 digits long!')
            else:
                raise ValidationError('Mobile number should only contain numbers(0-9) and be exactly 10 digits long!')


    def grade_from_percentage(self,percentage):
        grade=False
        if percentage:
            if percentage>=90 and percentage<=100:
                grade = 'A'
            elif percentage>=80 and percentage<90:
                grade = 'B'
            elif percentage>=70 and percentage<80:
                grade = 'C'
            elif percentage>=60 and percentage<70:
                grade = 'D'
            elif percentage>=50 and percentage<60:
                grade = 'E'   
            elif percentage<50:
                grade = 'F'
        return grade
    
    def _compute_total_percentage_grade(self):
        for record in self:
            if record.first_results:
                total_marks = 0
                obtained_marks = 0
                for result in record.first_results:
                    total_marks+=result.total_marks
                    obtained_marks+=result.obtained_marks
                record.first_total = obtained_marks
                if total_marks>0:
                    record.first_percentage = (obtained_marks/total_marks)*100
                    record.first_grade = self.grade_from_percentage(record.first_percentage)
                else:
                    record.first_percentage = 0
                    record.first_grade = False 

            else:
                record.first_total = 0
                record.first_percentage = 0
                record.first_grade = False  

            if record.second_results:
                total_marks = 0
                obtained_marks = 0
                for result in record.second_results:
                    total_marks+=result.total_marks
                    obtained_marks+=result.obtained_marks
                record.second_total = obtained_marks
                if total_marks>0:
                    record.second_percentage = (obtained_marks/total_marks)*100
                    record.second_grade = self.grade_from_percentage(record.second_percentage)
                else:
                    record.second_percentage = 0
                    record.second_grade = False
            else:
                record.second_total = 0
                record.second_percentage = 0
                record.second_grade = False  

            if record.final_results:
                total_marks = 0
                obtained_marks = 0
                for result in record.final_results:
                    total_marks+=result.total_marks
                    obtained_marks+=result.obtained_marks
                record.final_total = obtained_marks
                if total_marks>0:
                    record.final_percentage = (obtained_marks/total_marks)*100
                    record.final_grade = self.grade_from_percentage(record.final_percentage)
                else:
                    record.final_percentage = 0
                    record.final_grade = False
            else:
                record.final_total = 0
                record.final_percentage = 0
                record.final_grade = False  

    def assign_rollno(self):
        if not self.rollno:
            self.rollno = self.env['ir.sequence'].next_by_code('student.details')