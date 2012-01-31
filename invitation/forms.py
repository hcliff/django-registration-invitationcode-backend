from django import forms
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationForm
from registration.backends.invitation.fields import InvitationCodeField, ReCaptchaField

attrs_dict = {'class': 'required'}

class RegistrationFormBasic(RegistrationForm):
    """
    Purely validates the username, nothing else
    """
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # hide password 2 unless it's added back by mixin passwordmatch
        self.fields.pop('password2')

    def clean(self):
        pass
      
class RegistrationFormPasswordMatch(RegistrationFormBasic):
    """
    Require the user to enter the same password twice
    """
    
    # can't call it password2, will get removed by the parent close
    passwordb = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label=_("Repeat Password"))

    def clean(self):
        super(RegistrationFormPasswordMatch, self).clean()
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'passwordb' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['passwordb']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

class RegistrationFormUniqueEmail(RegistrationFormBasic):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.
    
    """
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use."))
        return self.cleaned_data['email']

class RegistrationFormInvitationCode(RegistrationFormBasic):
    """
    Adds invitation_code
    """
    invitation_code = InvitationCodeField(required=True, max_length=5,
        label=_(u"Invitation code"))

class RegistrationFormTOS(RegistrationFormBasic):
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={ 'required': _("You must agree to the terms to register") })  
                                   
class RegistrationFormFullName(RegistrationFormBasic):
    """
    Adds a full_name field that is subsequently split into first and last name
    """
    full_name = forms.CharField(max_length=70, required=True, label='Full Name')
    
    def clean(self):
        super(RegistrationFormFullName, self).clean()
        if not len(self.cleaned_data.get('full_name', '')):
            self._errors['full_name'] = self.error_class(['We need your first and last name'])
        else:
            name_parts = self.cleaned_data['full_name'][:].strip().split(None, 1)
            
            if len(name_parts) != 2:
                self._errors['full_name'] = self.error_class(['We need your first and last name'])
            else:
                self.cleaned_data['first_name'], self.cleaned_data['last_name'] = name_parts
                
                if len(self.cleaned_data['first_name']) < 2:
                    self._errors['full_name'] = self.error_class(['First name is too short'])
                elif len(self.cleaned_data['last_name']) < 2:
                    self._errors['full_name'] = self.error_class(['Last name is too short'])
                
        return self.cleaned_data

class RegistrationFormReCaptcha(RegistrationFormBasic):
    """
    Adds a captcha to your registration form
    """
    recaptcha = ReCaptchaField( label=_("Captcha"))