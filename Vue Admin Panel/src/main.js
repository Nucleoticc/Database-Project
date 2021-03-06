import { createApp } from "vue";

import router from './router.js';
import store from './store/index.js';
import App from "./App.vue";
import 'bulma/css/bulma.css';

const app = createApp(App);

app.use(router);
app.use(store);

app.mount("#app");
