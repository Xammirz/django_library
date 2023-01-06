import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from library.models import BookInstance


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField()

    def clean_due_back(self):
        data = self.cleaned_data["renewal_date"]

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_("Недействительная дата\
                                    - продление в прошлом"))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _(
                    "Недействительная дата - продление в прошлую дату \
                     - продление более чем на 4 недели вперед"
                )
            )

        # Remember to always return the cleaned data.
        return data

    class Meta:
        model = BookInstance
        fields = ["due_back"]
        labels = {"due_back": _("New renewal date")}
        help_texts = {
            "due_back": _("Enter a date between now and 4 weeks (default 3).")
        }
