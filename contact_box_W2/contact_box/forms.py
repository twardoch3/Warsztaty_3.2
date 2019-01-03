from django.forms import ModelForm, Textarea, Form, ModelChoiceField, CharField, CheckboxSelectMultiple
from .models import Person, PhoneNumber, Address, Email, Group


class PersonForm(ModelForm):
    class Meta:
        model = Person
        exclude = ['address','width_field', 'height_field']
        widgets = {
            'description': Textarea(attrs={'cols': 30, 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['groups'].required = False
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


# address form 1
class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['apartment_number'].required = False
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


# address form 2
class AddressSelectForm(Form):
    address = ModelChoiceField(queryset=Address.objects.all(), empty_label=None, label='SELECT ADDRESS - city, street, building and apartment number')


class PhoneNumberForm(ModelForm):
    class Meta:
        model = PhoneNumber
        exclude = ['person']

    def __init__(self, *args, **kwargs):
        super(PhoneNumberForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class EmailForm(ModelForm):
    class Meta:
        model = Email
        exclude = ['person']

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class GroupForm(ModelForm):
    class Meta:
        model = Group
        exclude = ['person']

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


# seach form
class SearchFrom(Form):
    first_name = CharField(max_length=64, label='First name#', required=False)
    last_name = CharField(max_length=100, label='Last name#', required=False)
    city = CharField(max_length=100, label='City#', required=False)


# group form
class GroupSelectForm(ModelForm):
    class Meta:
        model = Person
        fields = ['groups']
        widgets = {
            'groups': CheckboxSelectMultiple
        }
