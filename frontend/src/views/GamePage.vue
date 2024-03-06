<template>
  <div>
    <div v-if="showTryForm">
      <TryForm :word="hand.id_word" @tryContent="sendTry" />
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
      showTryForm: false,
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
      let flag = false;
      const token = this.$cookieParser("token");
      const data = await fetch("api/game/start", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }).then((response) => {
        if (response.ok) flag = true;
        return response.json();
      });

      if (data && flag) this.handleGameData(data);
      else if (data) this.notification = data.message;
    },
    handleGameData(data) {
      if (!data.words) {
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

        if (data && data.id_word && data.started_at) {
          this.stopInterval();
          this.hand.id_word = data.id_word;
          this.hand.started_at = data.started_at;
          this.showTryForm = true;
        } else if (data) {
          this.notification = data.message;
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
    // Sen the user try...
    async sendTry(content) {
      const token = this.$cookieParser("token");

      const data = await fetch("api/try/add", {
        method: ["POST"],
        body: new URLSearchParams({ content: content }),
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }).then((response) => {
        if (response.ok) {
          this.showTryForm = false;
          // En realidad debería esperar a que el tiempo termine...
          this.startWaitingTime(this.fetchVotes);
        }
        return response.json();
      });

      if (data && data.message) this.notification = data.message;
    },
    async fetchVotes() {
      const token = this.$cookieParser("token");
      console.log("Looking for trys...");
      const data = await fetch("api/trys", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }).then((response) => response.json());

      if (data) {
        this.notification = data?.message ?? data;
        this.stopInterval();
      }
    },
  },
};
</script>

<style></style>
