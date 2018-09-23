<template>
  <div class="contact-list col-12 col-md-8 col-lg-6">
		<b-button variant="primary" class="button" v-if="!contactSelected" @click="addNewContact()">Add new</b-button>
		<div v-show="loading">
			<i class="fa fa-spinner fa-spin"/>
			<p>Loading</p>
		</div>
    <table v-show="!loading && !contactSelected" class="table table-hover table-dark">
			<thead>
				<tr>
					<th class="col-10 col-md-6 col-lg-4">Name</th>
					<th class="col-1"></th>
					<th class="col-1"></th>
				</tr>
			</thead>
			<tbody>
				<tr v-if="!contacts || contacts.length === 0">
					<td colspan="3">No contacts.</td>
				</tr>
				<template v-else-if="contacts.length > 0" v-for="contact in contacts">
					<tr :key="contact.id">
						<td class="col-10 col-md-6 col-lg-4">{{ contact.first_names ? contact.first_names + " " +  contact.last_name : contact.last_name}}</td>
						<td class="col-1"><a class="far fa-edit" @click="editContact(contact.id)" title="Edit contact"/></td>
						<td class="col-1"><a class="far fa-trash-alt" @click="deleteContact(contact)" title="Delete contact"/></td>
					</tr>
				</template>
			</tbody>
		</table>
		<ContactEdit v-if="contactSelected"/>
  </div>
</template>

<script>

// this is needed to get csrf token for axios
function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
			const cookies = document.cookie.split(';');
			for (let i = 0; i < cookies.length; i++) {
					const cookie = cookies[i].trim();
					// Does this cookie string begin with the name we want?
					if (cookie.substring(0, name.length + 1) === (name + '=')) {
							cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
							break;
					}
			}
	}
	return cookieValue;
}

const axios = require('axios')

export default {
  name: "ContactList",
  components: {
		// allow webpack code splitting
		ContactEdit: () => import('./ContactEdit')
  },
	data: function() {
		return {
			// true if data is loading
			loading: false
		}
	},
	/**
	 * Mounted hook: gets list of contacts from server
	 */
	mounted: function() {
		let v = this;

		v.loading = true;

		// returns a list of contacts
		axios.get('/getContactList/')
		.then(function(response) {
			v.$store.commit('updateContacts', response.data.contact_list)
			v.loading = false;

			// requesting getContactList will all install csrf cookie which we need for ajax
			axios.defaults.headers.post['X-CSRFToken'] = getCookie('csrftoken');
			axios.defaults.headers.delete['X-CSRFToken'] = getCookie('csrftoken');
		})
		.catch(function(response) {
			v.loading = false;
			console.warn('Couldn\'t get contacts:', response);
		});
	},
	computed: {
		/**
		 * @returns a list of contacts sorted by last name
		 */
		contacts () {
			let contactList = this.$store.state.contacts;

			if (contactList) {
				function compare(a, b) {
					if (a.last_name < b.last_name)
						return -1;
					if (a.last_name > b.last_name)
						return 1;
					return 0;
				}

				contactList.sort(compare);
			}
			return contactList;
		},
		/**
		 * @returns True if a contact is selected
		 */
		contactSelected () {
			return this.$store.state.contactSelected;
		}
	},
	methods: {
		/**
		 * Deletes a contact
		 * @param contact The contact to be deleted
		 */
		deleteContact: function (contact) {
			const confirmed = confirm("Are you sure you want to delete this contact?");

			// if user has confirmed they definetly want to do this
			if (confirmed) {
				let v = this;

				axios.delete('/contact?id=' + contact.id)
				.then(function (response) {
					console.log(response);
					alert("Contact deleted successfully.");
					
					//remove record
					const index = v.contacts.indexOf(contact);
					if (index !== -1) {
							v.contacts.splice(index, 1);
					}
				})
				.catch(function (error) {
					console.warn(error);
					alert("Contact delete failed.");
				});
			}
		},
		/**
		 * Opens up edit form
		 * @param contactID ID of contact to be edited
		 */
		editContact: function (contactID) {
			this.$store.commit('updateSelectedContact', contactID);
			this.$store.commit('updateContactSelected', true);
		},
		/**
		 * Opens up create form
		 */
		addNewContact: function () {
			this.$store.commit('updateContactSelected', true);
		}
	}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.contact-list {
	margin-left:auto; 
	margin-right:auto;
	text-align: left;
}

.far:hover {
  font-size: 1.3em;
	cursor: pointer;
}

.button {
	margin-bottom: 10px;
	float: right;
}
</style>
