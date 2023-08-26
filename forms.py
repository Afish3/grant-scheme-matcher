from wtforms import SelectField, StringField, TextAreaField, FileField, IntegerField, BooleanField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional
from flask import session, jsonify

questions = ['question', 
             'next question', 
             'next question', 
             'next question', 
             'final question']

states = ["Land Management Plan", "Habitat Protectioin", "Deer Management", "Woodlands In and Around Towns", "Low Impact Silvicultural Systems"]


class GrantForm(FlaskForm):
    q1 = StringField('Question')
    q2 = StringField('next question')
    q3 = StringField('next question')
    q4 = StringField('next question')
    q5 = StringField('final question')
    submit = SubmitField('Next')

    @classmethod
    def get_next_question(cls, form):
        current_question = session.get('current_question', 0)

        if current_question < len(questions):
            question = questions[current_question]
            field_name = f'q{current_question + 1}'
            return jsonify({"question": question, 
                            "form": str(getattr(form, field_name))})
        else:
            return jsonify({"question": None})

    # croft = BooleanField("you a tenant, owner-occupier, sub-tenant, or short-lease holder of a registered croft approved by the Crofting Commission?", validators=[Optional()])

    # name = StringField("Name of Area",  validators=[
    #                    InputRequired(message="Snack Name can't be blank")])
    
    # price = IntegerField("How Much Money Do You Need?")
    # quantity = IntegerField("How many hectares of land?")
    # is_healthy = BooleanField("This is on private land")

    # state = SelectField('Type of project', choices=[(st, st) for st in states])