<template>
  <div>
    <div v-if="hand.id_word">
      <TryForm :word="hand.id_word" />
    </div>
    <div v-else-if="words.length > 0">
      <WordSelector :words="words" @get-word="wordSelected" />
    </div>
    <div v-else>
      <div>{{ notification }}</div>
    </div>
  </div>
</template>

<script>
import WordSelector from "@/components/WordSelector.vue";
import TryForm from "@/components/TryForm.vue";

export default {
  components: {
    WordSelector,
    TryForm,
  },
  data() {
    return {
      notification: "",
      waitingTime: 3000, // Miliseconds
      waitingTimeID: null,
      words: [],
      hand: {
        id_word: null,
        started_at: "",
      },
    };
  },
  created() {
    const token = this.$cookieParser("token");
    const id_game = this.$cookieParser("id_game");

    if (!token) this.notification = "You must login first...";
    else if (!id_game) this.notification = "You must enter a game first...";
    else this.startWaitingTime(this.fetchGameData);
  },
  methods: {
    startWaitingTime(fun) {
      if (this.waitingTimeID) this.stopInterval();
      this.waitingTimeID = setInterval(fun, this.waitingTime);
    },
    stopInterval() {
      clearInterval(this.waitingTimeID);
    },
    // Handle the first interaction...
    async fetchGameData() {
      console.log("Fetching data...");
      const token = this.$cookieParser("token");
      const data = await fetch("api/game/start", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }).then((response) => response.json());

      if (data) {
        this.handleGameData(data);
      }
    },
    handleGameData(data) {
      if (!data.words) {
        this.notification = data.message;
        this.words = [];
        this.startWaitingTime(this.handleHandWaiting);
      } else if (data.words) {
        this.words = data.words;
        this.stopInterval();
      }
    },
    // Until the leader select the word...
    async handleHandWaiting() {
      const token = this.$cookieParser("token");
      console.log("Waiting...");

      if (this.words.length == 0) {
        const response = await fetch("api/hand", {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        const data = await response.json();

        if (data) {
          this.stopInterval();
          this.hand.id_word = data.id_word;
          this.hand.started_at = data.started_at;
        }
      }
    },
    // Handle the word selection...
    async wordSelected(word) {
      const token = this.$cookieParser("token");
      fetch("api/hand/start", {
        method: ["POST"],
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: new URLSearchParams({ word: word }),
      }).then((response) => {
        if (response.ok) {
          this.words = [];
          this.handleHandWaiting();
        }
      });
    },
  },
};
</script>

<style></style>
