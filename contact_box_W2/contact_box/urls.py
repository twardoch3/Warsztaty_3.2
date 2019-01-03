from django.urls import path
from .views import AddEditPersonView, DeletePersonView, ShowAllPersonsView, ShowOnePersonView, AddEditAddressView, \
    DeleteAddressView, AddEditPhoneNumberView, DeletePhoneNumberView, AddEditEmailView, DeleteEmailView, \
    AddEditGroupView, DeleteGroupView, GroupsListView, SearchResultsView, AddContactView, AddPersonGroupView, RemovePersonAddressView

urlpatterns = [
    # contact persons
    path('person/new', AddEditPersonView.as_view(), name='new_person'),
    path('person/<int:id>/edit', AddEditPersonView.as_view(), name='edit_person'),
    path('person/<int:pk>/delete', DeletePersonView.as_view(), name='delete_person'),
    path('person/<int:id>', ShowOnePersonView.as_view(), name='person_details'),

    #contact
    path('contact/new', AddContactView.as_view(), name='new_contact' ),

    path('', ShowAllPersonsView.as_view(), name='all_persons'),
    path('person/address/<int:person_id>', AddEditAddressView.as_view(), name='person_address'),
    path('person/address/remove/<int:person_id>',RemovePersonAddressView.as_view(),name='remove_person_address'), #usuniecie addresu
    path('address/delete/<int:pk>', DeleteAddressView.as_view(), name='delete_address'),
    path('person/group/<int:person_id>', AddPersonGroupView.as_view(), name='person_choose_group'),

    # phone_number
    path('person/phone_number/new/<int:person_id>', AddEditPhoneNumberView.as_view(), name='new_phone_number'),
    path('person/phone_number/<int:person_id>/<int:pn_id>', AddEditPhoneNumberView.as_view(), name='edit_phone_number'),
    path('phone_number/delete/<int:pk>', DeletePhoneNumberView.as_view(), name='delete_phone_number'),

    # email
    path('person/email/new/<int:person_id>', AddEditEmailView.as_view(), name='new_email'),
    path('person/email/<int:person_id>/<int:email_id>', AddEditEmailView.as_view(), name='edit_email'),
    path('email/delete/<int:pk>', DeleteEmailView.as_view(), name='delete_email'),

    # groups
    path('groups/', GroupsListView.as_view(), name='list_of_groups'),
    path('group/new', AddEditGroupView.as_view(), name='new_group'),
    path('group/edit/<int:id>', AddEditGroupView.as_view(), name='edit_group'),
    path('group/delete/<int:pk>', DeleteGroupView.as_view(), name='delete_group'),

    #search
    path('search_results/', SearchResultsView.as_view() , name='search_results')

]
