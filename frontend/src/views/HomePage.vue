<template>
  <div>
    <GameDisplayer
      :gameNumber="1"
      :userConnected="2"
      :maxUser="5"
    ></GameDisplayer>
    <GameDisplayer
      :gameNumber="1"
      :userConnected="2"
      :maxUser="5"
    ></GameDisplayer>
    <GameDisplayer
      :gameNumber="1"
      :userConnected="2"
      :maxUser="5"
    ></GameDisplayer>
  </div>
</template>

<script>
import GameDisplayer from "@/components/GameDisplayer.vue";

export default {
  name: "HomePage",
  components: {
    GameDisplayer,
  },
};
</script>

<style></style>
