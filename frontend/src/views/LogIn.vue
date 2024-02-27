<template>
  <div>
    <form-component
      :buttonLabel="label"
      :fields="loginField"
      @onClick="check_data"
    ></form-component>
    <transition>
      <div v-if="error != ''">
        {{ error }}
      </div>
    </transition>
  </div>
</template>
<script>
import FormComponent from "@/components/FormComponent.vue";

export default {
  name: "LogIn",
  components: {
    FormComponent,
  },
  data() {
    return {
      loginField: [
        { name: "email", placeHolder: "Email", type: "text" },
        { name: "password", placeHolder: "Password", type: "password" },
      ],
      error: "",
      label: "Log In",
    };
  },
  methods: {
    async check_data(inputsData) {
      // Check empty inputs...
      this.error = this.check_json(inputsData);
      if (this.error != "") return;

      // Send the data...
      const data = {
        email: inputsData.email,
        password: inputsData.password,
      };

      const json = await fetch("api/login", {
        method: "POST",
        body: new URLSearchParams(data),
      }).then((response) => response.json());

      // If the token was received...
      if (json.access_token) {
        this.error = "";
        // Save the token as a cookie...
        document.cookie = `token=${json.access_token}; path=/; SameSite=None; Secure`;
      } else {
        this.error = json?.message ?? "Error";
      }
    },
    check_json(json) {
      for (let element in json)
        if (json[element] == "")
          return `The field ${element} must not be empty`;
      return "";
    },
  },
};
</script>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.1s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
