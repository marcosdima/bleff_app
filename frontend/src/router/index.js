import { createRouter, createWebHashHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import LogIn from "../views/LogIn.vue";
import RegisterPage from "../views/RegisterPage.vue";
import GameSelection from "../views/GameSelection.vue";

const routes = [
  {
    path: "/",
    name: "HomePage",
    component: HomePage,
  },
  {
    path: "/login",
    name: "LogIn",
    component: LogIn,
  },
  {
    path: "/register",
    name: "RegisterPage",
    component: RegisterPage,
  },
  {
    path: "/game/selection",
    name: "GameSelection",
    component: GameSelection,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
