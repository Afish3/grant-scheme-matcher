from wtforms import SelectField, StringField, TextAreaField, FileField, IntegerField, BooleanField, SubmitField, RadioField, SelectMultipleField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional
from flask import session, jsonify, render_template

questions = ["Are you a tenant, owner-occupier, sub-tenant, or short-lease holder of the land", 
             "If you are a sub-tenant, have you obtained the principal tenant's permission for any improvement works you intend to carry out?", 
             "If this land is currently being used, what is it being used for?", 
             "Ownership of the Land", 
             'Is/Are the owner(s) all under the age of 41?', 
             'Do you plan to create new native woodlands with this grant?',
             "Do you plan to restore 'ghost woodlands' '(former native woodlands that have been degraded  to less than 20% canopy cover but still retain ecological potential)'",
             "Do you plan to plant trees?",
             "What is the size of your land?",
             "What do you hope to see come out of this project?",
             "Is your land located in the South of Scotland near the Scottish Borders?"]

states = ["Land Management Plan", "Habitat Protectioin", "Deer Management", "Woodlands In and Around Towns", "Low Impact Silvicultural Systems"]

land_uses = ['croft / farm', 'commercial', 'private land, personnal use', 'public land']

ownership_types = ['The land is individually owned', 'The land is group owned']

land_sizes = ['Less than 0.25 hectares', 'Between 3 and 5 hectares', 'Between 3 and 100 hectares']

hopes_for_project = ['Imporvements to my croft (agricultural buildings, sewage, etc.)',                   'Improvement of farm animal well-being', 
                     'Improvement of ecological and habitat robustness', 
                     'Increasing carbon stores through halting degradation and loss of native woodland', 
                     'Natural flood management', 
                     'other']

class GrantForm(FlaskForm):
    q1 = SelectField(questions[0], choices=['Yes', 'No'])
    # q1 = SelectField('Question', choices=[st for st in states])
    q2 = SelectField(questions[1], choices=['Yes', 'No'])
    q3 = SelectField(questions[2], choices = [use for use in land_uses])
    q4 = SelectField(questions[3], choices = [own for own in ownership_types])
    q5 = SelectField(questions[4], choices=['Yes, all owners are under the age of 41', 'No'])
    q6 = SelectField(questions[5], choices=['Yes', 'No'])
    q7 = SelectField(questions[6], choices=['Yes', 'No'])
    q8 = SelectField(questions[7], choices=['Yes', 'No'])
    q9 = SelectField(questions[8], choices=[size for size in land_sizes])
    q10 = SelectField(questions[9], choices=[hope for hope in hopes_for_project])
    q11 = SelectField(questions[10], choices=['Yes, my land is in the south of Scotland', 'No'])


    @classmethod
    def get_next_question(cls, form, num):

        if num-1 < len(questions):
            question = questions[num-1]
            field_name = f'q{num}'

            field_html = str(getattr(form, field_name))
            form_html = f''' 
                            <div class="form-group row">
                                <div class="col-sm-10">
                                {field_html}
                                </div>
                            </div>
                        '''

            return jsonify({"question": question, 
                            "form": form_html})
        else:
            return None