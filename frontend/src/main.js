import { createApp } from "vue";
import App from "./App.vue";
import router from "@/router";
import { VueTelegramPlugin } from "vue-tg";

const app = createApp(App);
app.use(router);
app.use(VueTelegramPlugin);
app.mount("#app");
