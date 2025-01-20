import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../views/LoginPage.vue";
import HomePage from "../views/HomePage.vue";
import AuthPage from "../views/AuthPage.vue";
import FileUploadPage from "../views/FileUploadPage.vue";

// Define your routes
const routes = [
  {
    path: "/login",
    name: "Login",
    component: LoginPage,
  },
  {
    path: "/",
    name: "Home",
    component: HomePage,
  },
  {
    path: "/auth",
    name: "Auth",
    component: AuthPage,
  },
  {
    path: "/fileupload",
    name: "FileUpload",
    component: FileUploadPage,
  },
];

// Create the router instance
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // Use the HTML5 History mode
  routes,
});

export default router;
