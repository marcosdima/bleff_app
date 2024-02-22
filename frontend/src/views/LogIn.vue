<template>
  <div class="body">
    <input class="element" type="text" placeholder="Email" v-model="email" />
    <input
      class="element"
      type="text"
      placeholder="Password"
      v-model="password"
    />
    <custom-button class="element" @click="check_data"> Log In </custom-button>
    <transition>
      <div v-if="error != ''">
        {{ error }}
      </div>
    </transition>
  </div>
</template>
<script>
import CustomButton from "@/components/CustomButton.vue";

export default {
  name: "LogIn",
  components: {
    CustomButton,
  },
  data() {
    return {
      email: "",
      password: "",
      isVisible: false,
      error: "",
    };
  },
  methods: {
    async check_data() {
      // Check empty inputs...
      if (this.email == "") {
        this.error = "The field Email must not be empty";
        return;
      } else if (this.password == "") {
        this.error = "The field Password must not be empty";
        return;
      } else {
        // Send the data...
        const data = {
          email: this.email,
          password: this.password,
        };

        const json = await fetch("api/login", {
          method: "POST",
          body: new URLSearchParams(data),
        }).then((response) => response.json());

        // If the token was received...
        if (json.access_token) {
          this.error = "";
          // Save the token as a cookie...
          document.cookie = `token=${json.access_token}; path=/;`;
        } else {
          this.error = json?.message ?? "Error";
        }
      }
    },
  },
};
</script>

<style scoped>
.body {
  display: flex;
  flex-direction: column;
  margin: 100px;
}

.element {
  margin: 10px;
  width: 30%;
  align-self: center;
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.1s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
