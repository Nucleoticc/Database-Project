<template>
  <navbar v-if="isLoggedIn"></navbar>
  <router-view v-slot="slotProps">
    <transition name="route" mode="out-in">
      <component :is="slotProps.Component"></component>
    </transition>
  </router-view>
</template>

<script>
import Navbar from './components/TheNavBar/Navbar.vue';
export default {
  components:{
    Navbar
  },
  computed: {
    isLoggedIn(){
      return this.$store.getters['isAuthenticated']
    }
  },
  created(){
    this.$store.dispatch('tryLogin');
  },
};
</script>

<style>
:root{
  font-size: 16px;
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
  --text-primary: #b6b6b6;
  --text-secondary: #ececec;
  --bg-primary: #23232e;
  --bg-secondary: #141418;
}

main {
  margin-left: 5rem;
  padding: 1rem;
}

body{
  color: black;
  background-color: white;
  margin: 0;
  padding: 0;
}

body::-webkit-scrollbar{
  width: 0.25rem;
}

body::-webkit-scrollbar-track{
  background: #1e1e24;
}

body::-webkit-scrollbar-thumb{
  background: 6649b8;
}

.route-enter-from {
  opacity: 0;
  transform: translateY(-30px);
}
.route-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.route-enter-active {
  transition: all 0.3s ease-out;
}

.route-leave-active {
  transition: all 0.3s ease-in;
}

.route-enter-to,
.route-leave-from{
  opacity: 1;
  transform: translateY(0);
}
</style>
