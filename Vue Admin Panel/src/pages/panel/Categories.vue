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
    setData() {
      return this.$store.getters["categories/categories"];
    },
  },
  methods: {
    async loadCategories(refresh = false) {
      try {
        await this.$store.dispatch("categories/loadCategories", {
          forceRefresh: refresh,
        });
      } catch (error) {
        this.error = error.message || "Something Went Wrong!";
      }
    },
  },
  data() {
    return {
      headers: ["ID", "Name", "Description", "Status"],
    };
  },
  created() {
    this.loadCategories();
  },
};
</script>

<style scoped></style>
