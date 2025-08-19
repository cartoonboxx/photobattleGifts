import { createRouter, createWebHistory } from "vue-router";
import PricePageComponent from "@/page/prize/PricePageComponent.vue";

const routes = [{ path: "/prize/:id", component: PricePageComponent }];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
