<template>
  <div class="form-body">
    <div v-for="field in fields" :key="field.name">
      <input
        class="form-element"
        :type="field.type"
        :placeholder="field.placeHolder"
        v-model="formData[field.name]"
        @input="handleInput(field.name, $event.target.value)"
      />
    </div>
    <button class="form-element" @click="onClick">{{ buttonLabel }}</button>
  </div>
</template>

<script>
export default {
  name: "FormComponent",
  emits: ["onClick"],
  props: {
    fields: {
      type: Array,
      required: true,
      validator(array) {
        // The array has to have objects with the properties: name, type and placeHolder.
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
  data() {
    return { formData: {} };
  },
  methods: {
    handleInput(fieldName, value) {
      this.formData[fieldName] = value;
    },
    onClick() {
      this.$emit("onClick", this.formData);
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
