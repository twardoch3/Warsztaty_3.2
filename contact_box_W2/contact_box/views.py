from .models import Person, Address, PhoneNumber, Email, Group
from django.views import View
from django.views.generic.list import ListView
from django.views.generic import DeleteView
from .forms import PersonForm, PhoneNumberForm, AddressForm, EmailForm, GroupForm, AddressSelectForm, SearchFrom, \
    GroupSelectForm
from django.shortcuts import render, redirect, get_object_or_404


class ShowAllPersonsView(ListView):
    model = Person
    template_name = 'contact_box/base.html'
    paginate_by = 20  # !!!!
    ordering = ['last_name', 'first_name']


class AddContactView(View):
    def get(self, request):
        form_p = PersonForm()
        form_a_db = AddressSelectForm()
        form_a = AddressForm()
        form_pn = PhoneNumberForm()
        form_em = EmailForm()
        ctx = {'form_p': form_p, 'form_a': form_a, 'form_pn': form_pn, 'form_em': form_em, 'form_a_db': form_a_db}
        return render(request, 'contact_box/new_contact_full_form.html', ctx)

    def post(self, request):
        form_p = PersonForm(request.POST, request.FILES)
        form_pn = PhoneNumberForm(request.POST)
        form_em = EmailForm(request.POST)
        form_a_db = AddressSelectForm(request.POST)
        form_a = AddressForm(request.POST)
        person = None
        form_list = [form_p.is_valid(), form_em.is_valid(), form_pn.is_valid()]
        if all(form_list):
            # person
            form_p.save()
            person = form_p.instance
            # pnumber
            form_pn.instance.person = person
            form_pn.save()
            # email
            form_em.instance.person = person
            form_em.save()
            if form_a.is_valid():
                # address
                form_a.save()
                person.address = form_a.instance
                person.save()  # albo update!
                return redirect(form_p.instance)
            else:
                a1 = None
                if request.POST.get('building_number') and request.POST.get('apartment_number'):
                    a1 = Address.objects.filter(city=request.POST.get('city'),
                                                street=request.POST.get('street'),
                                                building_number=request.POST.get('building_number'),
                                                apartment_number=request.POST.get('apartment_number'))

                if a1:
                    person.address = a1[0]
                    person.save()  # !!!
                else:
                    if form_a_db.is_valid():
                        person.address = form_a_db.cleaned_data[
                            'address']  # Address.objects.get(pk=form_a_db.cleaned_data['address'])
                        person.save()
                return redirect(form_p.instance)

        ctx = {'form_p': form_p, 'form_a': form_a, 'form_pn': form_pn, 'form_em': form_em, 'form_a_db': form_a_db}
        return render(request, 'contact_box/new_contact_full_form.html', ctx)


class AddEditPersonView(View):
    def get(self, request, id=None):
        t = 'add new PERSON'
        form = PersonForm()
        if id:
            t = 'edit PERSON'
            p = get_object_or_404(Person, pk=id)
            form = PersonForm(instance=p)
        ctx = {'form': form, 't': t}
        return render(request, 'contact_box/person.html', ctx)

    def post(self, request, id=None):
        t = 'Add New Person'
        form = PersonForm(request.POST, request.FILES)
        if id:
            t = 'Edit Person'
            p = get_object_or_404(Person, pk=id)
            form = PersonForm(request.POST, request.FILES, instance=p)
        ctx = {'form': form, 't': t}
        if form.is_valid():
            form.save()
            return redirect(form.instance)  # redirect('all_persons')
        else:
            return redirect(request, 'contact_box/person.html', ctx)


class ShowOnePersonView(View):
    def get(self, request, id):
        person = get_object_or_404(Person, pk=id)
        form = AddressForm()
        address = person.address
        phone_numbers = PhoneNumber.objects.filter(person=person)
        emails = Email.objects.filter(person=person)
        ctx = {'form': form, 'person': person, 'address': address, 'phone_numbers': phone_numbers, 'emails': emails}
        return render(request, 'contact_box/person_details.html', ctx)


class DeletePersonView(DeleteView):
    model = Person
    success_url = '/contacts'


class AddEditAddressView(View):
    def get(self, request, person_id):
        person = get_object_or_404(Person, pk=person_id)
        address = Address.objects.filter(person=person)
        form_a = AddressForm()
        form_a_db = AddressSelectForm()
        select = True
        if address:
            form_a = AddressForm(instance=address[0])
            form_a_db = None
            select = False
        ctx = {'form_a': form_a, 'person': person, 'form_a_db': form_a_db, 'select': select}
        return render(request, 'contact_box/address.html', ctx)

    def post(self, request, person_id):
        person = get_object_or_404(Person, pk=person_id)
        address = Address.objects.filter(person=person)
        form_a = AddressForm(request.POST)
        form_a_db = AddressSelectForm(request.POST)
        select = True

        if address:
            form_a = AddressForm(request.POST, instance=address[0])
            select = False
        if form_a.is_valid():
            form_a.save()
            person.address = form_a.instance
            person.save()
            return redirect(person)
        elif form_a_db.is_valid():
            person.address = form_a_db.cleaned_data['address']
            person.save()
            return redirect(person)

        ctx = {'form_a': form_a, 'person': person, 'form_a_db': form_a_db, 'select': select}
        return render(request, 'contact_box/address.html', ctx)


class DeleteAddressView(DeleteView):
    model = Address
    success_url = '/contacts/'

class RemovePersonAddressView(View):
    def get(self, request, person_id):
        person = get_object_or_404(Person, pk=person_id)
        person.address = None
        person.save()
        return redirect(person)


class AddEditPhoneNumberView(View):
    def get(self, request, person_id, pn_id=None):
        person = get_object_or_404(Person, pk=person_id)
        form = PhoneNumberForm()
        if pn_id:
            phone_number = get_object_or_404(PhoneNumber, pk=pn_id)
            form = PhoneNumberForm(instance=phone_number)
        ctx = {'form': form, 'person': person}
        return render(request, 'contact_box/phone_number.html', ctx)

    def post(self, request, person_id, pn_id=None):
        person = get_object_or_404(Person, pk=person_id)
        form = PhoneNumberForm(request.POST)
        if pn_id:
            phone_number = get_object_or_404(PhoneNumber, pk=pn_id)
            form = PhoneNumberForm(request.POST, instance=phone_number)
        ctx = {'form': form, 'person': person}
        if form.is_valid():
            form.instance.person = person
            form.save()
            return redirect(person)
        return render(request, 'contact_box/phone_number.html', ctx)


class DeletePhoneNumberView(DeleteView):
    model = PhoneNumber
    success_url = '/contacts/'


class AddEditEmailView(View):
    def get(self, request, person_id, email_id=None):
        person = get_object_or_404(Person, pk=person_id)
        form = EmailForm()
        if email_id:
            email = get_object_or_404(Email, pk=email_id)
            form = EmailForm(instance=email)
        ctx = {'form': form, 'person': person}
        return render(request, 'contact_box/email.html', ctx)

    def post(self, request, person_id, email_id=None):
        person = get_object_or_404(Person, pk=person_id)
        form = EmailForm(request.POST)
        if email_id:
            email = get_object_or_404(Email, pk=email_id)
            form = EmailForm(request.POST, instance=email)
        ctx = {'form': form, 'person': person}
        if form.is_valid():
            form.instance.person = person
            form.save()
            return redirect(person)
        return render(request, 'contact_box/email.html', ctx)


class DeleteEmailView(DeleteView):
    model = Email
    success_url = '/contacts/'


class GroupsListView(ListView):
    model = Group
    template_name = 'contact_box/groups_list.html'
    paginate_by = 20
    ordering = ['group_name']


class AddEditGroupView(View):
    def get(self, request, id=None):
        form = GroupForm()
        if id:
            group = get_object_or_404(Group, pk=id)
            form = GroupForm(instance=group)
        ctx = {'form': form}
        return render(request, 'contact_box/group.html', ctx)

    def post(self, request, id=None):
        form = GroupForm(request.POST)
        if id:
            group = get_object_or_404(Group, pk=id)
            form = GroupForm(request.POST, instance=group)
        ctx = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('list_of_groups')
        return render(request, 'contact_box/group.html', ctx)


class DeleteGroupView(DeleteView):
    model = Group
    success_url = '/contacts/'


class AddPersonGroupView(View):
    def get(self, request, person_id):
        groups = Group.objects.all()
        person = get_object_or_404(Person, pk=person_id)
        form = GroupSelectForm(instance=person)
        ctx = {'form': form, 'person': person, 'groups': groups}
        return render(request, 'contact_box/person_groups.html', ctx)

    def post(self, request, person_id):
        groups = Group.objects.all()
        person = get_object_or_404(Person, pk=person_id)
        form = GroupSelectForm(request.POST, instance=person)
        ctx = {'form': form, 'person': person, 'groups': groups}
        if form.is_valid():
            form.save()
            return redirect(person)
        return render(request, 'contact_box/person_groups.html', ctx)


class SearchResultsView(View):
    def get(self, request):
        form = SearchFrom(request.GET)
        ctx = {}
        if form.is_valid():
            fn = form.cleaned_data['first_name']
            ln = form.cleaned_data['last_name']
            c = form.cleaned_data['city']
            if fn == '' and ln == '' and c == '':
                ctx['searched_persons'] = None
            else:
                ctx = {'fn': fn, 'ln': ln, 'c': c}
                ctx['searched_persons'] = Person.search_objects.search(fn, ln, c)

        return render(request, 'contact_box/search_results.html', ctx)
