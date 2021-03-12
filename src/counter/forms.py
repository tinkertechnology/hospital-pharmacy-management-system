from django import forms


class CounterForm(forms.Form):
    name = forms.CharField(max_length=30)
    slug = forms.EmailField(max_length=254)
    # message = forms.CharField(
    #     max_length=2000,
    #     widget=forms.Textarea(),
    #     help_text='Write here your message!'
    # )
    # source = forms.CharField(
    #     max_length=50,
    #     widget=forms.HiddenInput()
    # )

    def clean(self):
        cleaned_data = super(CounterForm, self).clean()
        name = cleaned_data.get('name')
        slug = cleaned_data.get('slug')
        # message = cleaned_data.get('message')
        if not name and not email:
            raise forms.ValidationError('You have to write something!')


# class ColorfulCounterForm(forms.Form):
#     name = forms.CharField(
#         max_length=30,
#         widget=forms.TextInput(
#             attrs={
#                 'style': 'border-color: blue;',
#                 'placeholder': 'Enter name here'
#             }
#         )
#     )
#     email = forms.EmailField(
#         max_length=254,
#         widget=forms.TextInput(attrs={'style': 'border-color: green;'})
#     )
#     message = forms.CharField(
#         max_length=2000,
#         widget=forms.Textarea(attrs={'style': 'border-color: orange;'}),
#         help_text='Write here your message!'
#     )