from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template import Context, loader
from django.template.loader import render_to_string, get_template




def send_confirm_mail(user, email):

    mail_subject = 'Activate your VoteNow account'
    context = {'user':user}
    message = loader.get_template('accounts/email.html').render(context)
    to_email = email
    from_email = 'noreply@votenow.xyz'
    msg = EmailMessage(mail_subject, message, to=[to_email],from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()