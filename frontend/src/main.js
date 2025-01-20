import { createApp } from "vue";
import * as bootstrap from "bootstrap/dist/js/bootstrap.bundle";
import router from "./router";
import "./style.css";
import App from "./App.vue";

const app = createApp(App);
app.provide("bootstrap", bootstrap);
app.use(router);
app.mount("#app");
