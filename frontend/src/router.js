import { createRouter, createWebHistory } from "vue-router";
import PricePageComponent from "@/page/prize/PricePageComponent.vue";
import App from "@/App.vue";

const routes = [
  { path: "/", component: App },
  { path: "/prize/:id", component: PricePageComponent },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
