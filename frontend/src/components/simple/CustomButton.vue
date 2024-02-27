<template>
  <div
    class="button"
    :style="{ background: backgroundColor }"
    @mouseenter="backgroundColor = mouseOnColor"
    @mouseleave="backgroundColor = mouseOutColor"
  >
    <FontAwesomeIcon
      class="icon"
      :icon="iconName"
      size="3x"
      v-if="iconName != ''"
    ></FontAwesomeIcon>
    <div class="icon" v-if="label != ''">{{ label }}</div>
  </div>
</template>

<script>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
export default {
  components: {
    FontAwesomeIcon,
  },
  props: {
    iconName: {
      type: String,
      default: "plus",
    },
    label: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      backgroundColor: "palegoldenrod",
      mouseOnColor: "darkgray",
      mouseOutColor: "palegoldenrod",
    };
  },
};
</script>

<style scoped>
.button {
  display: flex;
  align-content: center;
  justify-content: center;
  border: solid blueviolet;
  width: 20%;
  border-radius: 10px;
}
</style>
