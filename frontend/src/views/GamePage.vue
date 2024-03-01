<template>
  <div>
    {{ notification }}
  </div>
</template>

<script>
export default {
  data() {
    return {
      notification: "",
      waitingTime: 3000, // Miliseconds
      waitingTimeID: null,
      words: [],
      hand: null,
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
      if (this.waitingTimeID) this.stopInterval(this.waitingTimeID);
      this.waitingTimeID = setInterval(fun, this.waitingTime);
    },
    stopInterval() {
      clearInterval(this.waitingTimeID);
    },
    async fetchGameData() {
      console.log("Fetching data...");
      const token = this.$cookieParser("token");
      fetch("api/game/start", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }).then((response) => {
        if (response.ok) this.handleGameData(response.json());
      });
    },
    handleGameData(data) {
      if (data.message) {
        this.notification = data.message;
        this.words = [];
        this.startWaitingTime(this.handleHandWaiting);
      } else if (data.words) {
        this.words = data.words;
        this.stopInterval();
      }
    },
    // This function should be used by the no leader players..
    async handleHandWaiting() {
      const token = this.$cookieParser("token");
      if (!this.words) {
        fetch("api/hand", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }).then((response) => {
          if (response.ok) {
            this.hand = response.json();
            this.stopInterval();
          }
        });
      }
    },
  },
};
</script>

<style></style>
