from allauth.account.forms import SignupForm
from django import forms
from django.contrib import messages
from django.core.validators import FileExtensionValidator
from django.db import DatabaseError, transaction

from core.models import Document, Description


class SimpleSignupForm(SignupForm):
    description = forms.CharField()
    document = forms.FileField(validators=[FileExtensionValidator(["pdf"])])

    def save(self, request):
        with transaction.atomic():
            # create new user
            user = super().save(request)

            # save document and description
            description = self.cleaned_data['description']
            document = self.cleaned_data['document']

            Description.objects.create(user=user, text=description, is_active=False)
            Document.objects.create(user=user, file=document, is_active=False)
            return user
