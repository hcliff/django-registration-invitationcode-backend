from django import forms
from django.conf import settings
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

from registration.backends.invitation.widgets import ReCaptcha
from registration.backends.invitation.models import InvitationCode

from recaptcha.client import captcha

class InvitationCodeField(forms.CharField):
    """Invitation code field"""

    def validate(self, value):
        """Validate against invitation code table"""
        super(InvitationCodeField, self).validate(value)

        try:
            invitation_code = InvitationCode.objects.get(is_used=False,
                code=value)
        except InvitationCode.DoesNotExist:
            raise forms.ValidationError(_("Invalid invitation code."))

"""
Simple wrapper for reCaptcha
allows use of ReCaptchaForm input
http://djangosnippets.org/snippets/1653/
"""
class ReCaptchaField(forms.CharField):
    default_error_messages = {
        'captcha_invalid': 'Invalid captcha'
    }

    def __init__(self, *args, **kwargs):
        self.widget = ReCaptcha
        self.required = True
        super(ReCaptchaField, self).__init__(*args, **kwargs)

    def clean(self, values):
        
        super(ReCaptchaField, self).clean(values[1])
        
        recaptcha_challenge_value = smart_unicode(values[0])
        recaptcha_response_value = smart_unicode(values[1])
        
        check_captcha = captcha.submit(recaptcha_challenge_value, recaptcha_response_value, settings.RECAPTCHA_PRIVATE_KEY, {})
        
        if not check_captcha.is_valid:
            raise forms.util.ValidationError(self.error_messages['captcha_invalid'])
        return values[0]