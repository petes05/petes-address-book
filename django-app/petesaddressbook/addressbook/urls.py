from addressbook.views import ContactListView, HomeView, ContactView
from django.urls import path
from django.contrib.auth import views as auth_views

app_name="addressbook"

urlpatterns = [
  path('', HomeView.as_view(), name='home'),
	path('getContactList/', ContactListView.as_view(), name='get_contact_list'),
	path('contact', ContactView.as_view(), name='contact'),
]