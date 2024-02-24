<template>
  <FormComponent
    :fields="registrationField"
    :buttonLabel="label"
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
        { name: "email", placeHolder: "Email", type: "text" },
        { name: "password", placeHolder: "Password", type: "password" },
      ],
      label: "Register",
    };
  },
};
</script>

<style scoped></style>
