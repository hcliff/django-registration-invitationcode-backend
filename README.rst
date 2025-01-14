Invitation code backend for django-registration
===============================================

This is custom backend for `django-registration`_.

Features of backend:

* requires invitation code to proceed,
* requires TOS (Terms of Service) accepted by user.
* requires a full name provided by the user
* requires a ReCaptcha

Invitation codes are useful for e.g. service beta testing.
Also, since backend is fully compatibile with default backend, when your service is going public and you decide not to use invitation codes, all you need to do is turn "default" backend on.

Mixin all the things
--------------------

All the forms are mixins, each provides something, construct the form you want from the various mixins.

In your forms.py file::

    from registration.backends.invitation.forms import *

    class RegistrationForm(RegistrationFormFullName, RegistrationFormInvitationCode, RegistrationFormReCaptcha):
        pass
      
This is your form, it requires a valid username (mandatory), a full name, an invitation code and a captcha.
      
then in your urls.py file::


    from forms import RegistrationFormSpling
    from registration.views import register

    urlpatterns = patterns('',
        url(r'^accounts/register/', register,
            {'backend': 'registration.backends.invitation.InvitationBackend',
            'form_class': RegistrationForm},
            name='registration_register'),
        (r'^accounts/', include('spling.registration.backends.invitation.urls') ),
    )


Installation
------------

1. Copy invitation directory contents to your django-registration backends - such as registration/backends/invitation/

2. In settings.py INSTALLED_APPS section add 'registration.backends.invitation' after 'registration'::

    INSTALLED_APPS = (
        'registration',
        'registration.backends.invitation',
    )

3. You must change your urls.py where you are invoking registration (check project main urls.py)::

    (r'^accounts/', include('registration.backends.invitation.urls'), ),

4. Run syncdb or south schemamigration if you use it::

    ./manage.py syncdb

Invitation code
---------------

Application created InvitationCode model for codes. Invitation codes can be anything you want - here there are 5 random characters.

InvitationCode model also stores information about who and when used specific code so you can track it.

Sample invitation code generation
---------------------------------

You can make invitation code as long as you want (change max_length in InvitationCode model if you want it to be longer than 5).

Sample code for generation::

    import string
    import random
    
    def generate_random_string():
        chars = string.letters + string.digits
        return "".join(random.sample(chars, 5))

Locale
------

Application provides translation for languages:

* Polish (pl)

To create new translation simply run::

    django-admin.py makemessages -l <language_code>

Requirements
------------

* `django-registration`_

.. _django-registration: http://bitbucket.org/ubernostrum/django-registration/
