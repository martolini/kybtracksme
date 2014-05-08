from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from kybsal.slave.models import Slave
from django import forms
from django.utils.html import strip_tags

class SlaveCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))
 
    def is_valid(self):
        form = super(SlaveCreationForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all_':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form
 
    class Meta:
        fields = ['email', 'username', 'first_name', 'last_name', 'password1',
                  'password2']
        model = Slave

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            Slave.objects.get(username=username)
        except Slave.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

class SlaveChangeForm(forms.ModelForm):
    new_password = forms.CharField()
    # new_avatar = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(SlaveChangeForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

    def save(self, *args, **kwargs):
        reader = super(SlaveChangeForm, self).save(commit=False)
        if self.cleaned_data['new_password']:
            reader.set_password(self.cleaned_data['new_password'])
        reader.save()
        return reader


    class Meta(UserChangeForm.Meta):
        fields = ['first_name', 'last_name', 'new_password']
        model = Slave