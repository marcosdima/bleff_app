<template>
  <div>
    <GameDisplayer
      :gameNumber="1"
      :userConnected="2"
      :maxUser="5"
    ></GameDisplayer>
    <CustomButton iconName="plus"></CustomButton>
    <WordComponent word="CASA" meaning="Lugar de dormicion"></WordComponent>
    <WordSelectorVue
      :words="[
        'HOME',
        'EPHEMERAL',
        'VERNACULAR',
        'OBFUSCATE',
        'MYRIAD',
        'PROCLIVITY',
      ]"
      @get-word="print"
    ></WordSelectorVue>
  </div>
</template>

<script>
import GameDisplayer from "@/components/GameDisplayer.vue";
import CustomButton from "@/components/simple/CustomButton.vue";
import WordComponent from "@/components/simple/WordComponent.vue";
import WordSelectorVue from "@/components/WordSelector.vue";

export default {
  name: "HomePage",
  components: {
    GameDisplayer,
    CustomButton,
    WordComponent,
    WordSelectorVue,
  },
  methods: {
    print(str) {
      console.log(str);
    },
  },
};
</script>

<style></style>
