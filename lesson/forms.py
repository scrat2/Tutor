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
