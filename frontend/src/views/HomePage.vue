<template>
  <div>
    <GameDisplayer
      :gameNumber="1"
      :userConnected="2"
      :maxUser="5"
    ></GameDisplayer>
    <CustomButton iconName="plus"></CustomButton>
  </div>
</template>

<script>
import GameDisplayer from "@/components/GameDisplayer.vue";
import CustomButton from "@/components/simple/CustomButton.vue";

export default {
  name: "HomePage",
  components: {
    GameDisplayer,
    CustomButton,
  },
};
</script>

<style></style>
