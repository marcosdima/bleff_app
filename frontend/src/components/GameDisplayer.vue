<template>
  <div
    :class="containerClass"
    @mouseenter="mouseOn = true"
    @mouseleave="mouseOn = false"
    @click="$emit('enter-game', gameNumber)"
  >
    <h1 class="con-element">{{ gameNumber }}</h1>
    <userConnected
      class="con-element"
      :maxUser="maxUser"
      :userTotal="userConnected"
    />
  </div>
</template>

<script>
import UserConnected from "./simple/UserConnected.vue";
export default {
  components: {
    UserConnected,
  },
  emits: ["enter-game"],
  data() {
    return {
      mouseOn: false,
    };
  },
  computed: {
    containerClass() {
      return {
        container: true,
        "container-mouse-on": this.mouseOn,
        "container-mouse-out": !this.mouseOn,
      };
    },
  },
  props: {
    gameNumber: {
      type: Number,
      default: 1,
    },
    userConnected: {
      type: Number,
      default: 1,
    },
    maxUser: {
      type: Number,
      default: 1,
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-content: center;
  flex-direction: row;
  flex-wrap: wrap;
  border: solid blueviolet;
  border-radius: 10px 20px 10px 20px;
  background: palegoldenrod;
}
.container-mouse-on {
  background: gray;
}
.container-mouse-out {
  background: palegoldenrod;
}
.con-element {
  margin: 0 10px 0 10px;
}
h1 {
  margin: 0;
}
</style>
