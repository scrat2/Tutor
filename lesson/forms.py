from django import forms


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT"
        super().__init__(**kwargs)


class TimeInput(forms.TimeInput):
    input_type = "time"

    def __init__(self, **kwargs):
        kwargs["format"] = "%H:%M"
        super().__init__(**kwargs)


class ConnexionForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
        max_length=30,
        required=True
    )

    password = forms.CharField(
        label='Password',
        max_length=50,
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )


listProm = (("ING1", u"ING1"), ("ING2", u"ING2"), ("IR3", u"IR3"), ("IR4", u"IR4"), ("IR5", u"IR5"),
            ("SEP3", u"SEP3"), ("SEP4", u"SEP4"), ("SEP5", u"SEP5"), ("IRA3", u"IRA3"), ("IRA4", u"IRA4"),
            ("IRA5", u"IRA5"), ("SEPA3", u"SEPA3"), ("SEPA4", u"SEPA4"), ("SEPA5", u"SEPA5"),
            (None, u"Promo"))

listCampus = (("ANGERS", u"ANGERS"), ("AIX", u"AIX"), (None, u"Campus"))


class ProfileForm(forms.Form):
    promo = forms.ChoiceField(
        choices=listProm,
        required=False
    )

    campus = forms.ChoiceField(
        choices=listCampus,
        required=False
    )


class LessonForm(forms.Form):
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nom du cours'}),
        max_length=30,
        required=True
    )

    subject = forms.CharField(
        label='Subject',
        widget=forms.Textarea(attrs={'class': 'form-input', 'name': 'sujet', 'rows': '2', 'cols': '62',
                                     'placeholder': 'Description / Sujet'}),
        max_length=200,
        required=True
    )

    room = forms.CharField(
        label='Room',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Lieu du cours'}),
        max_length=30,
        required=True
    )

    date = forms.DateField(
        label='date',
        widget=DateInput,
        required=True
    )

    begin = forms.TimeField(
        label='begin',
        widget=TimeInput,
        required=True
    )

    end = forms.TimeField(
        label='end',
        widget=TimeInput,
        required=True
    )

    promo = forms.ChoiceField(
        choices=listProm,
        required=True
    )

    campus = forms.ChoiceField(
        choices=listCampus,
        required=True
    )


class SearchForm(forms.Form):
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nom du cours'}),
        max_length=30,
        required=False
    )

    date = forms.DateField(
        label='date',
        widget=DateInput,
        required=False
    )

    promo = forms.ChoiceField(
        choices=listProm,
        required=False
    )

    campus = forms.ChoiceField(
        choices=listCampus,
        required=False
    )
