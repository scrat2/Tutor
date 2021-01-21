from django import forms


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


class ProfileForm(forms.Form):
    promo = forms.ChoiceField(
        choices=(("ING1", u"ING1"), ("ING2", u"ING2"), ("IR3", u"IR3"), ("IR4", u"IR4"), ("IR5", u"IR5"),
                 ("SEP3", u"SEP3"), ("SEP4", u"SEP4"), ("SEP5", u"SEP5"), ("IRA3", u"IRA3"), ("IRA4", u"IRA4"),
                 ("IRA5", u"IRA5"), ("SEPA3", u"SEPA3"), ("SEPA4", u"SEPA4"), ("SEPA5", u"SEPA5"),
                 (None, u"Veuillez choisir")),
        required=False
    )

    campus = forms.ChoiceField(
        choices=(("ANGERS", u"ANGERS"), ("AIX", u"AIX"),
                 (None, u"Veuillez choisir")),
        required=False
    )
