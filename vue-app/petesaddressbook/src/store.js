import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
		// list of contacts
		contacts: [],
		// id of selected contact
		selectedContact: undefined,
		// true if a contact is selected
		contactSelected: false
	},
  mutations: {
		updateContacts(state, contacts) {
			state.contacts = contacts;
		},
		addContactToList(state, contact) {
			state.contacts.push(contact);
		},
		updateContactName(state, updatedContact) {
			let contactToUpdate = state.contacts.find( contact => contact.id === updatedContact.id );
			contactToUpdate.first_names = updatedContact.first_names;
			contactToUpdate.last_name = updatedContact.last_name;
		},
		updateSelectedContact(state, contact) {
			state.selectedContact = contact;
		},
		updateContactSelected(state, bool) {
			state.contactSelected = bool;
		}
	},
  actions: {}
});
