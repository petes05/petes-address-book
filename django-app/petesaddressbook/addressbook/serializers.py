from rest_framework.serializers import ModelSerializer, StringRelatedField, IntegerField

from addressbook.models import Contact, Address

class AddresssSerializer(ModelSerializer):

	id = IntegerField(required=False)

	class Meta:
		model = Address
		fields = ('id', 'first_line', 'second_line', 'town', 'county', 'country', 'postcode')

class ContactSerializer(ModelSerializer):

	addresses = AddresssSerializer(required=False, many=True)

	class Meta:
		model = Contact
		fields = ('id', 'first_names', 'last_name', 'phone_number', 'email_address', 'dob', 'addresses', 'created_on')

	def create(self, validated_data):
		# remove this field as it doesn't exist in Contact
		addresses = validated_data.get('addresses')

		if addresses:
			validated_data.pop('addresses')

		contact = Contact.objects.create(**validated_data)

		contact.save()

		# create record/s in Address
		if addresses:
			for address in addresses:
				Address.objects.create(contact=contact, **address)

		return contact
	
	''' This needs down manually because of the Address relationship '''
	def update(self, instance, validated_data):
		instance.first_names = validated_data.get('first_names', instance.first_names)
		instance.last_name = validated_data.get('last_name', instance.last_name)
		instance.phone_number = validated_data.get('phone_number', instance.phone_number)
		instance.email_address = validated_data.get('email_address', instance.email_address)
		instance.dob = validated_data.get('dob', instance.dob)
				
		instance.save()

		addresses = validated_data.get('addresses')

		if addresses:
			for address in addresses:
				id = address.get('id', None)
				
				# update existing address
				if id:
					item = Address.objects.get(id=id)
					item.first_line = address.get('first_line', item.first_line)
					item.second_line = address.get('second_line', item.second_line)
					item.town = address.get('town', item.town)
					item.county = address.get('county', item.county)
					item.country = address.get('country', item.country)
					item.postcode = address.get('postcode', item.postcode)
					item.save()
				# create new address
				else:
					address['contact']=instance
					newAddress = Address.objects.create(**address)
					newAddress.save()

			return instance