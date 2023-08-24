from wtforms import SelectField, StringField, TextAreaField, FileField, IntegerField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional

states = ["Land Management Plan", "Habitat Protectioin", "Deer Management", "Woodlands In and Around Towns", "Low Impact Silvicultural Systems"]


class AddSnackForm(FlaskForm):
    croft = BooleanField("you a tenant, owner-occupier, sub-tenant, or short-lease holder of a registered croft approved by the Crofting Commission?", validators=[Optional()])

    name = StringField("Name of Area",  validators=[
                       InputRequired(message="Snack Name can't be blank")])
    
    price = IntegerField("How Much Money Do You Need?")
    quantity = IntegerField("How many hectares of land?")
    is_healthy = BooleanField("This is on private land")

    state = SelectField('Type of project', choices=[(st, st) for st in states])