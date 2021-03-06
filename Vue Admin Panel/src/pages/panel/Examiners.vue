<template>
  <main>
    <the-table :headers="headers" :data="setData"></the-table>
  </main>
</template>

<script>
import theTable from "../../components/Table/Table.vue";
export default {
  components: {
    theTable,
  },
  computed: {
    setData(){
      return this.$store.getters['examiners/examiners']
    }
  },
  methods:{
    async loadExaminers(refresh = false) {
      try {
        await this.$store.dispatch('examiners/loadExaminers', {
          forceRefresh: refresh
        });
      } catch (error) {
        this.error = error.message || 'Something Went Wrong!';
      }
    },
  },
  data() {
    return {
      headers: [
        "ID",
        "Fname",
        "Lname",
        "Email",
        "Username"
      ],
    };
  },
  created() {
    this.loadExaminers();
  }
};
</script>

<style scoped></style>
