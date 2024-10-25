import { createRouter, createWebHistory } from "vue-router";
//vistas
import AdminLogin from "../views/AdminLogin.vue";
import UserRegister from "../views/UserRegister.vue";
import AdminPanel from "../views/AdminPanel.vue";
import VerifyUserEmail from "../views/VerifyUserEmail.vue";

const routes = [
  {
    path: "/", // Redirigir a la página de registro como página inicial
    redirect: { name: "UserRegister" },
  },
  {
    path: "/register",
    name: "UserRegister",
    component: UserRegister,
  },
  {
    path: "/verify/:uid/:token",
    name: "VerifyUserEmail",
    component: VerifyUserEmail,
  },
  {
    path: "/login",
    name: "AdminLogin",
    component: AdminLogin,
  },
  {
    path: "/admin",
    name: "AdminPanel",
    component: AdminPanel,
    meta: { requiresAuth: true },
  },
];

// Configuración del router para Vue 3
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Verificar autenticación para las rutas protegidas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const isSuperuser = localStorage.getItem("is_superuser") === "true";
  const isStaff = localStorage.getItem("is_staff") === "true";

  if (to.meta.requiresAuth) {
    if (!token || !isSuperuser || !isStaff) {
      next({ name: "AdminLogin" });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;

