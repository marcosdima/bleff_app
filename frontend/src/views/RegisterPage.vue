<template>
  <FormComponent
    :fields="registrationField"
    :buttonLabel="label"
    @onClick="register"
  ></FormComponent>
</template>

<script>
import FormComponent from "@/components/FormComponent.vue";

export default {
  name: "RegisterPage",
  components: {
    FormComponent,
  },
  data() {
    return {
      registrationField: [
        { name: "name", placeHolder: "Name", type: "text" },
        { name: "lastname", placeHolder: "Lastname", type: "text" },
        { name: "email", placeHolder: "Email", type: "text" },
        { name: "password", placeHolder: "Password", type: "password" },
      ],
      label: "Register",
    };
  },
  methods: {
    async register(inputsData) {
      // Check empty inputs...
      if (this.check_json(inputsData) != "") return;

      const data = {
        email: inputsData.email,
        name: inputsData.name,
        password: inputsData.password,
      };

      const json = await fetch("api/register", {
        method: "POST",
        body: new URLSearchParams(data),
      })
        .then((response) => response.json())
        .catch((error) => {
          return {
            message: `Error: ${error}`,
          };
        });

      console.log(json.message);
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

<style scoped></style>
