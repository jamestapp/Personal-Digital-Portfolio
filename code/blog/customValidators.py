from wtforms.validators import ValidationError
from datetime import datetime, date
from blog.models import SkillsToProjects
import os


#contains custom validation checks used with wtforms and flask admin

def minDateCheck(form, field):
    if field.data < date(1995, 12, 9):
        raise ValidationError('Date must be after 9-12-1995')

def maxDateCheck(form, field):
    if field.data > date.today():
        raise ValidationError('Date must be before today')

def startBeforeEnd(form, field):
    if not form.start_date.data < form.end_date.data:
        raise ValidationError('Start date must be before end date')

def skillProjectComboValid(form, field):
    project_id = form.project.data.id
    skill_id = form.skill.data.id
    links = SkillsToProjects.query.filter(SkillsToProjects.skill_id == skill_id, SkillsToProjects.project_id == project_id).all()
    if links:
        raise ValidationError('That project is already linked to that skill')

def imageFileValid(form, field):
    imageList = os.listdir(os.path.join('blog', 'static', 'img'))
    if form.path.data:
        imageList.append(form.path.data.filename)
    if form.image_file.data not in imageList:
        raise ValidationError('That image is not uploaded, please add it via the upload form')

def imageUploadFileValid(form, field):
    imageList = os.listdir(os.path.join('blog', 'static', 'img'))
    if form.path.data and form.path.data.filename in imageList:
        raise ValidationError('An image with that name is already uploaded here. Either delete the image or rename your file')