<template>
  <div class="flex-container">
    <CustomButton :iconName="iconName" @click="createGame" />
    <div>
      <div v-for="game in games" :key="game.id_game">
        <GameDisplayer
          :gameNumber="game.id_game"
          :userConnected="game.users"
          :maxUser="max"
          @enter-game="handleEnterGame"
          class="game-displayer"
        />
      </div>
    </div>
  </div>
</template>

<script>
import GameDisplayer from "@/components/GameDisplayer.vue";
import CustomButton from "@/components/simple/CustomButton.vue";
export default {
  components: {
    GameDisplayer,
    CustomButton,
  },
  data() {
    return {
      games: [],
      selected: null,
      max: 5,
      iconName: "plus",
    };
  },
  created() {
    this.fetch_game_data();
    this.maxU = this.get_max_users();
  },
  methods: {
    async fetch_game_data() {
      const games_data = await fetch("api/games", { method: "GET" }).then(
        (response) => response.json()
      );
      this.games = [];
      for (let data of games_data) this.games.push(data);
    },
    async get_max_users() {
      const data = await fetch("api/max_users", { method: "GET" }).then(
        (respose) => respose.json()
      );
      return data.max_users;
    },
    async handleEnterGame(id) {
      const token = this.$cookieParser("token");

      const form = {
        id_game: id,
      };

      const data = await fetch("api/game/in", {
        method: "POST",
        body: new URLSearchParams(form),
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => response.json())
        .catch((error) => console.log(error));

      if (data && data.message) this.$notify(data.message);
      // Save the token as a cookie...
      if (data) {
        document.cookie = `id_game=${id}; path=/; SameSite=None; Secure`;
        this.$router.push("/game/play");
      }
    },
    async createGame() {
      const token = this.$cookieParser("token");
      const data = await fetch("api/game/create", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }).then((response) => response.json());

      if (data.message) this.$notify(data.message);
      else if (data.id_game) {
        document.cookie = `id_game=${data.id_game}; path=/; SameSite=None; Secure`;
        this.$router.push("/game/play");
      }
    },
  },
};
</script>

<style>
.flex-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.game-displayer {
  margin: 5px;
}
</style>
