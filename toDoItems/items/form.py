from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import InputRequired




# FORM FOR ADDING NEW LIST ITEMS
class ItemForm(FlaskForm):
    itemName = StringField(validators = [InputRequired()])
    submit = SubmitField(label = 'Add')



# FORM FOR EDITING ITEM
class ItemEditForm(FlaskForm):
    itemName = StringField(label = "Itemname", validators = [InputRequired()])
    submit = SubmitField(label = 'Submit')