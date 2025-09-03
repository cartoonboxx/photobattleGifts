import { createRouter, createWebHistory } from "vue-router";
import PrizePageComponent from "@/page/prize/PrizePageComponent.vue";
import App from "@/App.vue";

const routes = [
  { path: "/", component: App },
  { path: "/prize/:id", component: PrizePageComponent },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
