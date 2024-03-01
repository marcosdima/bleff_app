<template>
  <transition>
    <div class="word" @click="$emit('getWord', this.word)">
      <h1>{{ word }}</h1>
      <p>{{ meaning }}</p>
    </div>
  </transition>
</template>

<script>
export default {
  emits: ["getWord"],
  props: {
    word: String,
    meaning: String,
  },
};
</script>

<style>
.word {
  background: lightcyan;
  display: flex;
  align-content: center;
  justify-content: center;
  flex-direction: column;
  border: solid lightcoral;
  border-radius: 30%;
  width: fit-content;
  padding: 1rem;
  margin-bottom: 0.2rem;
}
</style>
