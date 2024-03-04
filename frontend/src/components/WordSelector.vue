<template>
  <div class="word-display">
    <div v-for="word of wordsInfo" :key="word.word">
      <WordComponent
        :meaning="word.meaning"
        :word="word.word"
        @getWord="$emit('getWord', word.word)"
      />
    </div>
  </div>
</template>

<script>
import WordComponent from "./simple/WordComponent.vue";

export default {
  emits: ["getWord"],
  components: {
    WordComponent,
  },
  props: {
    words: Array,
  },
  data() {
    return {
      wordsInfo: [],
    };
  },
  created() {
    this.getWordsData();
  },
  methods: {
    async getWordsData() {
      const wordsData = await fetch("api/words").then((response) =>
        response.json()
      );

      this.wordsInfo = wordsData.filter((object) =>
        this.words.includes(object.word)
      );
    },
  },
};
</script>

<style>
.word-display {
  display: flex;
  justify-content: space-evenly;
  align-content: center;
  flex-direction: row;
  flex-wrap: wrap;
}
</style>
