import { createRouter, createWebHistory } from "vue-router";
import { defineAsyncComponent } from "vue";
import store from './store/index.js';

const Login = defineAsyncComponent(() =>
  import("./pages/Auth/AdminLogin.vue")
);

const BasePanel = defineAsyncComponent(() =>
import("./pages/BasePanel.vue")
);

const Students = defineAsyncComponent(() =>
import("./pages/panel/Students.vue")
);

const Examiners = defineAsyncComponent(() =>
import("./pages/panel/Examiners.vue")
);

const Categories = defineAsyncComponent(() =>
import("./pages//panel/Categories.vue")
);

const NotFound = defineAsyncComponent(() =>
import("./components/NotFound.vue")
);

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: '/base' },
    {
      path: "/login",
      component: Login,
      meta: { requiresUnauth: true }
    },
    {
      path: '/base',
      component: BasePanel,
      meta: { requiresAuth: true }
    },
    {
      path: '/student',
      component: Students,
      meta: { requiresAuth: true }
    },
    {
      path: '/examiner',
      component: Examiners,
      meta: { requiresAuth: true }
    },
    {
      path: '/categories',
      component: Categories,
      meta: { requiresAuth: true }
    },
    { path: '/:notFound(.*)', component: NotFound }
  ],
});

router.beforeEach((to, _, next) => {
  if(to.meta.requiresAuth && !store.getters.isAuthenticated){
    next({path:'/login'});
  }
  else if(to.meta.requiresUnauth && store.getters.isAuthenticated) {
    next({path:'/base'});
  }
  else{
    next();
  }
})

export default router;
