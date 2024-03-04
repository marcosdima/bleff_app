<template>
  <div class="try-container flex-container">
    <h1 class="word-title">The word is: {{ word }}</h1>
    <textarea :v-model="text" :placeholder="sentence"></textarea>
    <CustomButton iconName="paper-plane" />
  </div>
</template>

<script>
import CustomButton from "./simple/CustomButton.vue";

export default {
  emits: ["tryContent"],
  components: {
    CustomButton,
  },
  props: {
    word: String,
  },
  data() {
    return {
      text: "",
    };
  },
  computed: {
    sentence() {
      return `Write what do you think ${this.word} means`;
    },
  },
};
</script>

<style scoped>
.try-container {
  border: solid;
  width: fit-content;
}
textarea {
  min-width: 1000px;
  min-height: 500px;
}
</style>
