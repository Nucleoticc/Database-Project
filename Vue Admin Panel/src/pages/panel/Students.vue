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
      return this.$store.getters['students/students']
    }
  },
  methods:{
    async loadStudents(refresh = false) {
      try {
        await this.$store.dispatch('students/loadStudents', {
          forceRefresh: refresh
        });
      } catch (error) {
        this.error = error.message || 'Something Went Wrong!';
      }
    },
  },
  data(){
      return{
        headers: [
        "ID",
        "Fname",
        "Lname",
        "Email",
        "Username",
        "Attempted",
        "Solved",
        "Score"
      ]
      };
  },
  created() {
    this.loadStudents();
  }
};
</script>

<style scoped></style>
