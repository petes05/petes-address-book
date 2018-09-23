from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView

from rest_framework.parsers import JSONParser

from addressbook.models import Contact, Address
from addressbook.serializers import ContactSerializer

class HomeView(TemplateView):

	template_name = "addressbook/home.html"

class ContactListView(ListView):
	"""
	Retrieve list of contacts' names
	"""
	@method_decorator(ensure_csrf_cookie)
	def get(self, request):
		try:
			result = Contact.objects.all().values('id', 'first_names', 'last_name')
			return JsonResponse({'contact_list': list(result)})
		except Contact.DoesNotExist:
			return HttpResponse(status=404)

class ContactView(View):
	"""
	Retrieve, update or delete a single contact.
	"""

	def get_contact(self, contact_id):
		try:
			return Contact.objects.get(id=contact_id)
		except Contact.DoesNotExist:
			return HttpResponse(status=404)
			
	def get(self, request):
		contact_id = request.GET.get("id")
		contact = self.get_contact(contact_id)
		serializer = ContactSerializer(contact)
		return JsonResponse(serializer.data, safe=False)

	def post(self, request):
			
		data = JSONParser().parse(request)
		
		if (not 'id' in data) or (data.get("id") is 'undefined'):   # this is a new contact
			try:
				serializer = ContactSerializer(data=data)
			except Exception as error:
				print(error)
				print("test")
		else:   # this is an existing contact that is being updated
			contact = self.get_contact(data.get("id"))
			
			serializer = ContactSerializer(contact, data=data)
		
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	def delete(self, request):
		contact_id = request.GET.get("id")
		contact = self.get_contact(contact_id)
		contact.delete()
		return HttpResponse(status=204)