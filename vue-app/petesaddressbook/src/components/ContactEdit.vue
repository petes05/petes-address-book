<template>
  <div class="contact-edit">
    <div v-show="loading">
      <i class="fa fa-spinner fa-spin"/>
      <p>Loading</p>
    </div>
    <form class="form-horizontal" action="" @submit="onSubmit">
      <div class="form-row">
        <div class="fieldWrapper form-group col-6">
          <label for="first_names">First name/s</label>
          <input id="first_names" type="text" class="form-control" placeholder="First name/s" maxlength="100" v-model="contactDetails.first_names">
        </div>
        <div class="fieldWrapper form-group col-6">
          <label for="last_name">Last name</label>
          <input id="last_name" type="text" class="form-control" placeholder="Last name" maxlength="35" v-model="contactDetails.last_name" required>
        </div>
      </div>
      <div class="form-row">
        <div class="fieldWrapper form-group col-6">
          <label for="phone_number">Phone number</label>
          <input id="phone_number" type="tel" class="form-control" placeholder="Phone number" v-model="contactDetails.phone_number">
        </div>
        <div class="fieldWrapper form-group col-6">
          <label for="email">Email</label>
          <input id="email" type="email" class="form-control" placeholder="Email" v-model="contactDetails.email">
        </div>
      </div>
      <div class="form-row">
        <div class="fieldWrapper form-group col-5">
          <label for="dob">Date of birth</label>
          <input id="dob" type="date" class="form-control" placeholder="Date of birth" v-model="contactDetails.dob">
        </div>
      </div>
      <div class="form-row">
        <div class="fieldWrapper form-group col-12">
          <label for="address1">Address 1</label>
          <input id="address1" type="text" class="form-control" placeholder="Address 1" maxlength="200" v-model="contactDetails.addresses[0].first_line">
        </div>
      </div>
      <div class="form-row">
        <div class="fieldWrapper form-group col-12">
          <label for="address2">Address 2</label>
          <input id="address2" type="text" class="form-control" placeholder="Address 2" maxlength="200" v-model="contactDetails.addresses[0].second_line">
        </div>
      </div>
      <div class="form-row">
        <div class="fieldWrapper form-group col-6">
          <label for="town">Town</label>
          <input id="town" type="text" class="form-control" placeholder="Town" maxlength="50" v-model="contactDetails.addresses[0].town">
        </div>
        <div class="fieldWrapper form-group col-6">
          <label for="county">County</label>
          <input id="county" type="text" class="form-control" placeholder="County" maxlength="50" v-model="contactDetails.addresses[0].county">
        </div>
      </div>
      <div class="form-row">
        <div class="fieldWrapper form-group col-6">
          <label for="country">Country</label>
          <input id="country" type="text" class="form-control" placeholder="Country" maxlength="50" v-model="contactDetails.addresses[0].country">
        </div>
        <div class="fieldWrapper form-group col-6">
          <label for="postcode">Postcode</label>
          <input id="postcode" type="text" class="form-control" placeholder="Postcode" maxlength="10" v-model="contactDetails.addresses[0].postcode">
        </div>
      </div>
      <div class="form_buttons">
        <b-button type="button" variant="primary" @click="onSubmit">Save</b-button>
        <b-button variant="danger" @click="formCancel">Cancel</b-button>
      </div>
    </form>
  </div>
</template>

<script>

let axios = require('axios')

export default {
  name: "ContactEdit",
  props: {
  },
  data: function() {
    return {
      loading: false,
      // note: this is set to allow muliple address per contact, but at the moment only one address is possible
      contactDetails: { addresses: [{}] }
    }
  },
  /**
   * Mounted hook: gets contact info if needed
   */
  mounted: function() {
    let v = this;

    // this will be undefined if we are creating a new contact
    if (v.selectedContact) {
      v.loading = true;

      axios.get('/contact?id=' + this.selectedContact)
      .then(function(response) {
        let result = response.data;

        // treat every contact as if they have one address
        if (!result.addresses || result.addresses.length === 0)
          result.addresses = [{}];

        v.contactDetails = result;
        v.loading = false;
      })
      .catch(function(response) {
        v.loading = false;
        console.warn('Couldn\'t get contact:', response);
      });
    }
  },
  computed: {
    /**
     * @returns the contact being edited (blank if creating new)
     */
    selectedContact () {
      return this.$store.state.selectedContact;
    }
  },
  methods: {
    /**
     * Submit contact to server
     */
    onSubmit: function () {
      let v = this;

      // last name is required
      if (!this.contactDetails.last_name)
      {
        alert("You must include a last name.");
        return;
      }
      
      axios.post('/contact', this.contactDetails)
      .then(function (response) {

        // if this is a new contact, add it to the list of contacts in vuex
        if (!v.selectedContact) {
          v.$store.commit('addContactToList', { 
            id: response.data.id, 
            first_names: response.data.first_names, 
            last_name: response.data.last_name });
          
          alert("Contact created.");
        }
        // if this is an existing contact we may need to update the name
        else {
          v.$store.commit('updateContactName', { 
            id: response.data.id, 
            first_names: response.data.first_names, 
            last_name: response.data.last_name });
          
          alert("Contact updated.");
        }

        v.$store.commit('updateSelectedContact', undefined);
        v.$store.commit('updateContactSelected', false);
      })
      .catch(function (error) {
        console.warn(error);
        alert("Save failed.");
      });
    },
    /**
     * Cancel the form
     */
    formCancel: function () {
      this.$store.commit('updateSelectedContact', undefined);
      this.$store.commit('updateContactSelected', false);
    }
  }
};
</script>
