from wtforms import SelectField, StringField, TextAreaField, FileField, IntegerField, BooleanField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional
from flask import session, jsonify, render_template

questions = ['question', 
             'next question', 
             'next question', 
             'next question', 
             'next question', 
             'final question']

states = ["Land Management Plan", "Habitat Protectioin", "Deer Management", "Woodlands In and Around Towns", "Low Impact Silvicultural Systems"]


class GrantForm(FlaskForm):
    # q1 = BooleanField('question')
    q1 = SelectField('Question', choices=[st for st in states])
    q2 = BooleanField('next question')
    q3 = BooleanField('next question')
    q4 = StringField('next question')
    q5 = BooleanField('next question')
    q6 = StringField('final question')

    @classmethod
    def get_next_question(cls, form):
        current_question = session.get('current_question', 0)

        if current_question < len(questions):
            question = questions[current_question]
            field_name = f'q{current_question + 1}'

            field_html = str(getattr(form, field_name))
            # Render_template is used here to produce html of the form which includes the hidden field CSRF token for form validation
            form_html = render_template('form.html', form=form, field_html=field_html)

            session['current_question'] = current_question + 1
            return jsonify({"question": question, 
                            "form": form_html})
        else:
            return jsonify({"question": None})