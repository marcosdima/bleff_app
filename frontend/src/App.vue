<template>
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/login">Log In</router-link> |
    <router-link to="/register">Register</router-link> |
    <router-link to="/game/selection">Games</router-link> |
    <router-link to="/game/play">Play</router-link>
  </nav>
  <router-view />
</template>

<script>
export default {
  name: "App",
  methods: {
    token() {
      const cookies = document.cookie.split(";").map((cookie) => cookie.trim());
      const tokenCookie = cookies.find((cookie) => cookie.startsWith("token="));
      return tokenCookie ? tokenCookie.split("=")[1] : null;
    },
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
