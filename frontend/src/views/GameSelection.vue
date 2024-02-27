<template>
  <div class="flex-container">
    <CustomButton :iconName="iconName" />
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
      const data = await fetch("api/game/in", {
        method: "POST",
        body: new URLSearchParams({ id_game: id }),
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }).then((response) => response.json());

      if (data.message) this.$notify(data.message);
    },
  },
};
</script>

<style scoped>
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
