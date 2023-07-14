from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField,SubmitField,ValidationError,SelectField
from wtforms.validators import DataRequired, Length, Email
from app.models import User
from wtforms_validators import ActiveUrl, Alpha, AlphaDash, AlphaSpace,Integer,AlphaNumeric


class LoginForm(FlaskForm):
        email = StringField('Email',validators=[DataRequired(),Length(1,64),Email()])     
        email_password = PasswordField('Password',validators = [DataRequired()]) 
        remember_me = BooleanField('Keep me logged in.')
        account_submit = SubmitField('Log in')

class signupForm(FlaskForm):
        user_email = StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
        email_password = PasswordField('Password',validators = [DataRequired(),Length(1,64)])
        create_account = SubmitField('Create account.')
        
        def validate_email(self,user_email):
                user_email = User.query.filter_by(user_email = user_email.data).first()
                if user_email:
                        raise ValidationError('email already registered.')
class apiRequestUserForm(FlaskForm):
        id = StringField('Id',validators=[DataRequired()])
        email = StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
        password = StringField('Password',validators=[Length(1,64),Alpha()],render_kw={'style': 'width: 28ch'})
        first_name = StringField('First Name',validators=[Length(1,64)],render_kw={'style': 'width: 28ch'})
        last_name = StringField('Last Name',validators=[Length(1,64)],render_kw={'style': 'width: 28ch'})
        confirmed = BooleanField('confirmed',validators=[],render_kw={'style': 'width: 28ch'})
        address = StringField('Street Address',validators=[Length(1,64),AlphaNumeric()],render_kw={'style': 'width: 28ch'})
        city= StringField('City',validators=[Length(1,64),Alpha()],render_kw={'style': 'width: 28ch'})
        province= StringField('Province',validators=[Length(1,64),Alpha()],render_kw={'style': 'width: 28ch'})
        country = StringField('Country',validators=[Length(1,64),Alpha()],render_kw={'style': 'width: 28ch'})
        postal_code = StringField('Postal Code',validators = [Length(min=6,max=6),AlphaNumeric()],render_kw={'style': 'width: 28ch'})
        phone_number = StringField('Phone Number',validators=[Length(10,10),AlphaNumeric()],render_kw={'style': 'width: 28ch'})
        subscription = StringField('subscription type',validators=[AlphaNumeric()],render_kw={'style': 'width: 28ch'})
        customer_id = StringField('Customer Id',validators=[AlphaNumeric()],render_kw={'style': 'width: 28ch'})
        subscription_id = StringField('Subscription Id',validators=[AlphaNumeric()],render_kw={'style': 'width: 28ch'})
        scan = StringField('Scans',validators=[],render_kw={'style': 'width: 28ch'})
        active = BooleanField('Active',validators=[],render_kw={'style': 'width: 28ch'})
        sub_day = StringField('Subscription Day',validators=[AlphaNumeric()],render_kw={'style': 'width: 28ch'})
        is_admin = BooleanField('Is Admin',validators=[],render_kw={'style': 'width: 28ch'})
        api_submit = SubmitField('Request')     
class parkForm(FlaskForm):
        id = StringField('Id',validators=[DataRequired()])
        park = SelectField('ENTER CAMPGROUND.',choices=['','Alice Lake','Bamberton','Bear Creek','Beatton','Beaumont','Big Bar Lake','Birkenhead Lake','Blanket Creek','Bowron Lake','Bromley Rock',
                           'Carp Lake','Champion Lakes','Charlie Lake','Chiliwack Lake','Cowichan River','Crooked River','Cultus Lake','Dry Gulch','E.C. Manning','Elk Falls','Ellison','Englishman River Falls','Fillongley',
                           'Fintry','French Beach','Gladstone','Golden Ears','Gordon Bay','Green Lake','Herald','Horsefly Lake','Inland Lanke','Juan de Fuca','Juniper Beach',
                           'Kekuli Bay','Kentucky Alleyne','Kettle River','Kikomun Creek','Kleanza Creek','Kokanee Creek','Kootenay Lake',' Lac La Hache','Lac Le Jeune','Lakelse Lake','Liard River Hot Springs','Little Qualicum Falls',
                           'Lov  land Bay','Mabel Lake','Martha Creek','McDonald Creek','Meziadin Lake','Miracle Beach','Moberly Lake','Monck','Montague Harbour Marine','Morton Lake','Mount Fernie','Mount Robson','Moyie Lake','Nairn Falls',
                           'Newcastle Island Marine','North Thompson River','Okanagan Lake North','Okanagan Lake South','Otter Lake','Paarens Beach','Paul Lake','Porpoise Bay','Porteau Cove','Premier Lake','Prudhomme Lake','Purden Lake',
                           'Rathtrevor Beach','Red Bluff','Rolley Lake','Rosebery','Saltery Bay','Sasquatch','Shuswap Lake','Silver Lake','Skagit Valley','Smelt Bay','Sowchea Bay','Sproat Lake','Stamp River','Stemwinder','Strathcona',
                           'Summit Lake','Swan Lake','sw̓iw̓s (Haynes Point)','sx̌ʷəx̌ʷnitkʷ (Okanagan Falls)','Syringa','Ten Mile Lake','Tweedsmuir South','Tyhee Lake','Tā Ch’ilā (Boya Lake)','Wasa Lake','Wells Gray','Whiskers Point'],
                           validators=[DataRequired()],render_kw={'style': 'width: 28ch'})
        api_submit = SubmitField('Request')     
class siteForm(FlaskForm):
        park = SelectField('ENTER CAMPGROUND.',choices=['','Alice Lake','Bamberton','Bear Creek','Beatton','Beaumont','Big Bar Lake','Birkenhead Lake','Blanket Creek','Bowron Lake','Bromley Rock',
                           'Carp Lake','Champion Lakes','Charlie Lake','Chiliwack Lake','Cowichan River','Crooked River','Cultus Lake','Dry Gulch','E.C. Manning','Elk Falls','Ellison','Englishman River Falls','Fillongley',
                           'Fintry','French Beach','Gladstone','Golden Ears','Gordon Bay','Green Lake','Herald','Horsefly Lake','Inland Lanke','Juan de Fuca','Juniper Beach',
                           'Kekuli Bay','Kentucky Alleyne','Kettle River','Kikomun Creek','Kleanza Creek','Kokanee Creek','Kootenay Lake',' Lac La Hache','Lac Le Jeune','Lakelse Lake','Liard River Hot Springs','Little Qualicum Falls',
                           'Lov  land Bay','Mabel Lake','Martha Creek','McDonald Creek','Meziadin Lake','Miracle Beach','Moberly Lake','Monck','Montague Harbour Marine','Morton Lake','Mount Fernie','Mount Robson','Moyie Lake','Nairn Falls',
                           'Newcastle Island Marine','North Thompson River','Okanagan Lake North','Okanagan Lake South','Otter Lake','Paarens Beach','Paul Lake','Porpoise Bay','Porteau Cove','Premier Lake','Prudhomme Lake','Purden Lake',
                           'Rathtrevor Beach','Red Bluff','Rolley Lake','Rosebery','Saltery Bay','Sasquatch','Shuswap Lake','Silver Lake','Skagit Valley','Smelt Bay','Sowchea Bay','Sproat Lake','Stamp River','Stemwinder','Strathcona',
                           'Summit Lake','Swan Lake','sw̓iw̓s (Haynes Point)','sx̌ʷəx̌ʷnitkʷ (Okanagan Falls)','Syringa','Ten Mile Lake','Tweedsmuir South','Tyhee Lake','Tā Ch’ilā (Boya Lake)','Wasa Lake','Wells Gray','Whiskers Point'],
                           validators=[DataRequired()],render_kw={'style': 'width: 28ch'})
        id = StringField('Id',validators=[DataRequired()])
        sites = SelectField('Enter Site #. ',choices=[],validators=[],render_kw={'style': 'width: 28ch'})
        campground = SelectField('Enter Outer Campground . ',choices=[''],validators=[DataRequired()],render_kw={'style': 'width: 28ch'})
        inner_campground = SelectField('Enter inner Campground. ',choices=[''],validators=[],render_kw={'style': 'width: 28ch'})
        park_id = StringField('Park Id',validators=[DataRequired()])
        api_submit = SubmitField('Request')     