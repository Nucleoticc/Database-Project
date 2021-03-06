<template>
  <div class="column is-offset-4" style="width:500px">
    <div class="container has-text-centered">
      <h2 class="title">Login</h2>
      <login @save-data="saveData"></login>
    </div>
  </div>
</template>

<script>
import Login from "../../components/admin/LoginForm.vue";
export default {
  components: {
    Login,
  },
  methods: {
    saveData(data) {
      this.$store.dispatch("login", data);
    },
  },
};
</script>
