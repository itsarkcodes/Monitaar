from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional

class WebsiteForm(FlaskForm):
    url = StringField('Website URL', validators=[DataRequired()])
    start_time = StringField('Start Time (e.g., 9am or 09:00)', validators=[Optional()])
    end_time = StringField('End Time (e.g., 6pm or 18:00)', validators=[Optional()])
    slack_user_ids = StringField('Slack User IDs (comma-separated)', validators=[Optional()])
    tag_here = BooleanField('Tag @here in Slack')  # New field
    submit = SubmitField('Submit')
