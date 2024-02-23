<template>
  <div class="form-body">
    <div class="form-element" v-for="field in fields" :key="field.name">
      <input :type="field.type" :placeholder="field.placeHolder" />
    </div>
  </div>
</template>

<script>
export default {
  name: "FormComponent",
  props: {
    fields: {
      type: Array,
      required: true,
      validator(array) {
        let valid = true;
        for (let value of array.__v_raw) {
          if (!(value.name && value.type && value.placeHolder)) {
            valid = false;
          }
        }
        return valid;
      },
    },
    buttonLabel: {
      type: String,
      default: "Enter",
    },
  },
};
</script>

<style scoped>
.form-body {
  display: flex;
  flex-direction: column;
  margin: 100px;
}

.form-element {
  margin: 10px;
  width: 30%;
  align-self: center;
}
</style>
