<template>
  <div class="users-connected">
    <div v-for="index in maxUser" :key="index" id="user-con-container">
      <font-awesome-icon
        v-if="index <= userTotal"
        icon="user"
        class="element"
      />
      <font-awesome-icon
        v-else
        icon="user"
        style="color: darkgrey"
        class="element"
      />
    </div>
  </div>
</template>

<script>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
export default {
  components: {
    FontAwesomeIcon,
  },
  props: {
    maxUser: {
      type: Number,
      required: true,
    },
    userTotal: {
      type: Number,
      required: true,
    },
  },
};
</script>

<style scoped>
.users-connected {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  align-content: center;
}
.element {
  margin: 2px;
}
#user-con-container {
  display: inline-flex;
}
</style>
